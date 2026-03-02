import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. 보안 금고 세팅
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
            (블로그 리뷰 데이터의 문제점 분석)

            ###PROFIT_PREDICT###
            (위드멤버의 10가지 올인원 솔루션 적용 시 3개월 후 예상 매출 상승 범위를 AI가 판단해서 강력하게 제시해. 
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

                # 리포트 디자인 (폰트 및 레이아웃 개선)
                html_report = f"""
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
                <div style="padding: 20px; display: flex; flex-direction: column; align-items: center; background-color: #f8fafc;">
                    <style>
                        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
                        * {{ font-family: 'Pretendard', sans-serif; word-break: keep-all; overflow-wrap: break-word; line-height: 1.6; }}
                        .section-title {{ color: #1e3a8a; font-size: 18px; font-weight: 800; margin-bottom: 10px; }}
                        .ad-list {{ list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: 1fr; gap: 8px; }}
                        .ad-list li {{ background: #ffffff; padding: 12px 15px; border-radius: 8px; color: #0369a1; font-weight: 700; font-size: 15px; border: 1px solid #bae6fd; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
                    </style>
                    <div id="report-card" style="width: 100%; max-width: 800px; padding: 50px 40px; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 15px; box-shadow: 0px 10px 25px rgba(0,0,0,0.05);">
                        
                        <h1 style="text-align: center; color: #1e40af; font-size: 28px; font-weight: 900; margin-bottom: 5px;">📈 맞춤형 평판 진단 및 마케팅 제안서</h1>
                        <p style="text-align: center; color: #64748b; margin-bottom: 35px; font-size: 16px;">대상 매장: <strong style="color: #0f172a;">{place_name}</strong></p>

                        <div style="background: #fffbeb; border: 1px solid #fde68a; padding: 25px; border-radius: 12px; margin-bottom: 35px;">
                            <h4 style="color: #b45309; margin-top: 0; margin-bottom: 15px; font-size: 18px; font-weight: 800;">📌 네이버 플레이스 상위 노출 핵심 지표</h4>
                            <p style="color: #92400e; font-weight: 600; margin-bottom: 15px;">상위 노출은 다음 4가지 지표로 결정되며, 체계적인 관리가 필수입니다.</p>
                            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                                <span style="background: white; padding: 8px 16px; border-radius: 20px; border: 1px solid #fcd34d; color: #d97706; font-weight: 800; font-size: 14px;">① 리뷰 활성도</span>
                                <span style="background: white; padding: 8px 16px; border-radius: 20px; border: 1px solid #fcd34d; color: #d97706; font-weight: 800; font-size: 14px;">② 키워드 적합도</span>
                                <span style="background: white; padding: 8px 16px; border-radius: 20px; border: 1px solid #fcd34d; color: #d97706; font-weight: 800; font-size: 14px;">③ 최신성 지수</span>
                                <span style="background: white; padding: 8px 16px; border-radius: 20px; border: 1px solid #fcd34d; color: #d97706; font-weight: 800; font-size: 14px;">④ 체류 시간</span>
                            </div>
                        </div>

                        <div style="margin-bottom: 30px; border-left: 5px solid #3b82f6; padding-left: 15px;">
                            <h3 class="section-title">1. 방문자 리뷰 진단 및 문제점</h3>
                            <p style="color: #334155;">{v_diag}</p>
                        </div>

                        <div style="margin-bottom: 30px; background: #f1f5f9; padding: 20px; border-radius: 10px;">
                            <h3 style="color: #0f172a; font-size: 16px; font-weight: 800; margin-top: 0; margin-bottom: 10px;">🤖 AI 추천 고객 감동 답글 예시</h3>
                            <div style="color: #475569; font-weight: 500; white-space: pre-wrap;">{a_reply}</div>
                        </div>

                        <div style="margin-bottom: 35px; border-left: 5px solid #10b981; padding-left: 15px;">
                            <h3 style="color: #064e3b; font-size: 18px; font-weight: 800; margin-bottom: 10px;">2. 블로그 리뷰 분석</h3>
                            <p style="color: #334155;">{b_diag}</p>
                        </div>

                        <div style="background: #e0f2fe; padding: 30px; border-radius: 15px; border: 2px solid #7dd3fc; margin-bottom: 30px;">
                            <h3 style="color: #0284c7; font-size: 22px; font-weight: 900; margin-top: 0; margin-bottom: 20px; text-align: center;">💎 위드멤버 올인원 마케팅 솔루션</h3>
                            <ul class="ad-list">
                                <li>1. 네이버 플레이스 세팅 및 관리 (SEO 최적화)</li>
                                <li>2. 업체에 맞는 최적화 블로그 후보 검수 및 추천 리포트 제공</li>
                                <li>3. 매장 또는 업체 홍보용 영상 콘텐츠 제작</li>
                                <li>4. 제작 후 인스타그램 릴스, 유튜브 쇼츠 배포</li>
                                <li>5. Google Business Profile 신규 등록 및 리뷰 작성 10건</li>
                                <li>6. 카카오맵 리뷰 작성 10건</li>
                                <li>7. 광고 운영 결과에 대한 월간 리포트 제공</li>
                                <li>8. 네이버 플레이스 순위, 노출 변화 모니터링 및 유지 관리</li>
                                <li>9. 월 2회 기본 수정 (사진, 정보, 새소식)</li>
                                <li>10. Google, 카카오맵 정보 유지 및 관리</li>
                            </ul>
                        </div>

                        <div style="background: #eff6ff; padding: 25px; border-radius: 10px; border: 1px solid #bfdbfe; text-align: center;">
                            <h3 style="color: #1e40af; font-weight: 800; margin-top:0; margin-bottom: 15px;">🚀 솔루션 적용 시 3개월 후 예상 매출</h3>
                            <div style="font-size: 26px; font-weight: 900; color: #2563eb;">{p_predict}</div>
                        </div>

                        <p style="text-align: center; font-size: 18px; font-weight: 800; color: #1e293b; margin-top: 40px;">"{conclusion}"</p>
                    </div>
                    
                    <button onclick="downloadImage()" style="margin-top: 30px; padding: 15px 30px; font-size: 16px; font-weight: 800; color: #fff; background-color: #2b6cb0; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        📸 솔루션 제안서 이미지(.png) 다운로드
                    </button>
                </div>
                
                <script>
                function downloadImage() {{
                    const element = document.getElementById('report-card');
                    html2canvas(element, {{
                        scale: 2, 
                        backgroundColor: "#ffffff",
                        useCORS: true
                    }}).then(canvas => {{
                        let link = document.createElement('a');
                        link.download = '{place_name}_마케팅제안서.png';
                        link.href = canvas.toDataURL();
                        link.click();
                    }});
                }}
                </script>
                """
                components.html(html_report, height=1600, scrolling=True)

            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")
