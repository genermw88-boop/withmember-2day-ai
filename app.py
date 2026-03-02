import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. 보안 금고 세팅 (이미 마스터하신 방식!)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("보안 금고(Secrets)에 API 키가 설정되지 않았습니다.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="위드멤버 2일차 리뷰 진단기", page_icon="📝", layout="wide")

st.title("📝 위드멤버 2일차: 리뷰 평판 및 매출 성장 진단")
st.markdown("매장의 리뷰 상태를 분석하고, 위드멤버 솔루션 적용 시 예상 매출 성장률을 산출합니다.")

# 2. 사용자 입력 폼
with st.form("review_analysis_form"):
    col1, col2 = st.columns(2)
    with col1:
        place_name = st.text_input("매장명", placeholder="예: 콤마 봉천점")
        category = st.text_input("업종/메뉴", placeholder="예: 삼겹살 전문점")
    with col2:
        visit_reviews = st.number_input("현재 방문자 리뷰 수", min_value=0, step=1)
        blog_reviews = st.number_input("현재 블로그 리뷰 수", min_value=0, step=1)

    submitted = st.form_submit_button("🚀 정밀 평판 진단 및 매출 예측 실행")

# 3. AI 로직 및 리포트 생성
if submitted:
    if not place_name:
        st.error("매장명을 입력해주세요.")
    else:
        with st.spinner("AI가 지역 상권 데이터와 리뷰 평판을 분석 중입니다..."):
            
            prompt = f"""
            너는 대한민국 최고의 소상공인 마케팅 전략가야. 아래 데이터를 바탕으로 사장님께 드리는 '리뷰 평판 진단 리포트'를 작성해.
            모든 내용은 전문적이고 신뢰감 있는 톤으로 작성하며, HTML 태그나 특수기호 없이 오직 구분자(###)를 사용해서 답해.

            [입력 데이터]
            - 매장명: {place_name} ({category})
            - 방문자 리뷰: {visit_reviews}개
            - 블로그 리뷰: {blog_reviews}개

            ###VISIT_DIAG###
            (방문자 리뷰 수에 대한 객관적 진단과 수치 부족 시 발생할 수 있는 신뢰도 저하 문제점을 2줄로 작성)

            ###AI_REPLY###
            (사장님이 실제 사용할 수 있는 정중하고 감동적인 방문자 리뷰 답글 예시 2개를 작성. 하나는 감사 인사, 하나는 재방문 유도 중심)

            ###BLOG_DIAG###
            (블로그 리뷰 데이터의 문제점 분석 및 '위드멤버'에서 프리미엄 체험단 1달 10건을 직접 검수하여 퀄리티를 보장하겠다는 내용 포함)

            ###PROFIT_PREDICT###
            (아래 3가지 솔루션 적용 시 3개월 후 예상 매출 상승 범위를 AI가 판단해서 제시해. 
            1. 플레이스 최적화, 2. 구글/카카오맵 리뷰 10건, 3. 블로그 체험단 10건 및 유튜브/인스타 배포.
            형식: "현재 대비 약 OO% ~ OO% 상승 예상")

            ###CONCLUSION###
            (위 마케팅 패키지가 사장님 매장에 필요한 이유를 강조하는 결론 1줄)
            """

            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                res = response.text

                # 데이터 추출 함수
                def cut(tag, next_tag=None):
                    try:
                        p = res.split(tag)[1]
                        return p.split(next_tag)[0].strip() if next_tag else p.strip()
                    except: return "데이터 분석 중..."

                v_diag = cut("###VISIT_DIAG###", "###AI_REPLY###")
                a_reply = cut("###AI_REPLY###", "###BLOG_DIAG###")
                b_diag = cut("###BLOG_DIAG###", "###PROFIT_PREDICT###")
                p_predict = cut("###PROFIT_PREDICT###", "###CONCLUSION###")
                conclusion = cut("###CONCLUSION###")

                # 리포트 디자인
                html_report = f"""
                <div style="padding: 20px; font-family: 'Malgun Gothic', sans-serif; background-color: #f8fafc;">
                    <div id="report-card" style="max-width: 800px; margin: auto; background: white; padding: 40px; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
                        <h1 style="text-align: center; color: #1e40af; font-size: 28px; margin-bottom: 5px;">📈 평판 진단 및 매출 성장 예측</h1>
                        <p style="text-align: center; color: #64748b; margin-bottom: 40px;">대상 매장: <strong>{place_name}</strong></p>

                        <div style="margin-bottom: 30px; border-left: 5px solid #3b82f6; padding-left: 15px;">
                            <h3 style="color: #1e3a8a; margin-bottom: 10px;">1. 방문자 리뷰 진단 및 문제점</h3>
                            <p style="color: #334155; line-height: 1.6;">{v_diag}</p>
                        </div>

                        <div style="margin-bottom: 30px; background: #f1f5f9; padding: 20px; border-radius: 10px;">
                            <h3 style="color: #0f172a; font-size: 16px; margin-bottom: 10px;">🤖 AI 추천 고객 답글 예시</h3>
                            <div style="color: #475569; font-style: italic; white-space: pre-wrap;">{a_reply}</div>
                        </div>

                        <div style="margin-bottom: 30px; border-left: 5px solid #10b981; padding-left: 15px;">
                            <h3 style="color: #064e3b; margin-bottom: 10px;">2. 블로그 리뷰 분석 및 체험단 솔루션</h3>
                            <p style="color: #334155; line-height: 1.6;">{b_diag}</p>
                            <p style="margin-top: 10px; color: #059669; font-weight: bold;">✅ 위드멤버 특전: 프리미엄 체험단 월 10건 밀착 검수 진행</p>
                        </div>

                        <div style="margin-bottom: 30px; background: #eff6ff; padding: 25px; border-radius: 10px; border: 1px solid #bfdbfe; text-align: center;">
                            <h3 style="color: #1e40af; margin-bottom: 15px;">🚀 위드멤버 패키지 적용 시 3개월 후 예상 매출</h3>
                            <div style="font-size: 24px; font-weight: 800; color: #2563eb;">{p_predict}</div>
                            <p style="font-size: 13px; color: #64748b; margin-top: 10px;">*플레이스 최적화 + 구글/카카오맵 리뷰 + 블로그/영상 마케팅 통합 적용 시</p>
                        </div>

                        <p style="text-align: center; font-size: 18px; font-weight: bold; color: #1e293b; margin-top: 40px;">"{conclusion}"</p>
                    </div>
                </div>
                """
                components.html(html_report, height=1000, scrolling=True)

            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")