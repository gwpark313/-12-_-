import streamlit as st
import random

# ─── 페이지 설정 ───
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️", layout="centered")

# ─── 커스텀 CSS ───
st.markdown("""
<style>
    .stApp { max-width: 600px; margin: 0 auto; }
    div[data-testid="stVerticalBlock"] > div { padding: 0; }
    .result-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
        border-left: 4px solid #378ADD;
    }
    .result-card.gold { border-left-color: #EF9F27; }
    .result-card.silver { border-left-color: #B4B2A9; }
    .result-card.bronze { border-left-color: #D85A30; }
    .score-badge {
        display: inline-block;
        background: #378ADD;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
    }
    .menu-name { font-size: 18px; font-weight: 600; margin: 0; }
    .menu-detail { font-size: 13px; color: #666; margin: 4px 0 0 0; }
</style>
""", unsafe_allow_html=True)

# ─── 메뉴 데이터 ───
# allergens 키: 각 메뉴의 알레르기 유발 성분
# is_vegan 키: 비건 여부
menus = [
    # 한식
    {"name": "김치찌개", "category": "한식", "spicy": 3, "price": 3, "allergens": ["대두"], "is_vegan": False},
    {"name": "된장찌개", "category": "한식", "spicy": 1, "price": 3, "allergens": ["대두", "갑각류"], "is_vegan": False},
    {"name": "김치볶음밥", "category": "한식", "spicy": 3, "price": 2, "allergens": ["계란"], "is_vegan": False},
    {"name": "제육볶음", "category": "한식", "spicy": 4, "price": 3, "allergens": [], "is_vegan": False},
    {"name": "순두부찌개", "category": "한식", "spicy": 3, "price": 3, "allergens": ["대두", "계란"], "is_vegan": False},
    {"name": "비빔밥", "category": "한식", "spicy": 2, "price": 3, "allergens": ["계란", "대두"], "is_vegan": False},
    {"name": "불고기", "category": "한식", "spicy": 1, "price": 4, "allergens": ["대두"], "is_vegan": False},
    {"name": "떡볶이", "category": "한식", "spicy": 4, "price": 2, "allergens": ["밀", "대두"], "is_vegan": True},
    {"name": "잡채", "category": "한식", "spicy": 1, "price": 3, "allergens": ["대두", "밀"], "is_vegan": False},
    {"name": "삼겹살", "category": "한식", "spicy": 1, "price": 4, "allergens": [], "is_vegan": False},
    {"name": "갈비탕", "category": "한식", "spicy": 1, "price": 5, "allergens": [], "is_vegan": False},
    {"name": "콩나물국밥", "category": "한식", "spicy": 2, "price": 2, "allergens": ["대두"], "is_vegan": True},
    {"name": "닭갈비", "category": "한식", "spicy": 4, "price": 3, "allergens": ["대두", "밀"], "is_vegan": False},
    # 중식
    {"name": "짜장면", "category": "중식", "spicy": 1, "price": 2, "allergens": ["밀", "대두"], "is_vegan": False},
    {"name": "짬뽕", "category": "중식", "spicy": 4, "price": 2, "allergens": ["밀", "갑각류", "대두"], "is_vegan": False},
    {"name": "볶음밥", "category": "중식", "spicy": 1, "price": 2, "allergens": ["계란"], "is_vegan": False},
    {"name": "탕수육", "category": "중식", "spicy": 1, "price": 4, "allergens": ["밀", "대두"], "is_vegan": False},
    {"name": "마파두부", "category": "중식", "spicy": 5, "price": 2, "allergens": ["대두"], "is_vegan": True},
    {"name": "깐풍기", "category": "중식", "spicy": 2, "price": 4, "allergens": ["밀", "대두"], "is_vegan": False},
    # 일식
    {"name": "초밥", "category": "일식", "spicy": 1, "price": 4, "allergens": ["갑각류", "대두"], "is_vegan": False},
    {"name": "라멘", "category": "일식", "spicy": 3, "price": 3, "allergens": ["밀", "대두", "계란"], "is_vegan": False},
    {"name": "돈카츠", "category": "일식", "spicy": 1, "price": 3, "allergens": ["밀", "계란"], "is_vegan": False},
    {"name": "우동", "category": "일식", "spicy": 1, "price": 2, "allergens": ["밀", "대두"], "is_vegan": False},
    {"name": "카레", "category": "일식", "spicy": 2, "price": 2, "allergens": ["밀", "우유"], "is_vegan": False},
    {"name": "규동", "category": "일식", "spicy": 1, "price": 2, "allergens": ["대두"], "is_vegan": False},
    # 양식
    {"name": "파스타", "category": "양식", "spicy": 1, "price": 4, "allergens": ["밀", "우유"], "is_vegan": False},
    {"name": "스테이크", "category": "양식", "spicy": 1, "price": 5, "allergens": [], "is_vegan": False},
    {"name": "리조또", "category": "양식", "spicy": 1, "price": 4, "allergens": ["우유"], "is_vegan": False},
    {"name": "샐러드", "category": "양식", "spicy": 1, "price": 3, "allergens": [], "is_vegan": True},
    {"name": "햄버거", "category": "양식", "spicy": 1, "price": 3, "allergens": ["밀", "우유", "계란"], "is_vegan": False},
    {"name": "피자", "category": "양식", "spicy": 2, "price": 4, "allergens": ["밀", "우유"], "is_vegan": False},
    {"name": "오믈렛", "category": "양식", "spicy": 1, "price": 3, "allergens": ["계란", "우유"], "is_vegan": False},
    # 분식
    {"name": "김밥", "category": "분식", "spicy": 1, "price": 1, "allergens": ["계란", "대두"], "is_vegan": False},
    {"name": "라볶이", "category": "분식", "spicy": 4, "price": 2, "allergens": ["밀", "대두"], "is_vegan": False},
    {"name": "순대", "category": "분식", "spicy": 1, "price": 2, "allergens": ["밀"], "is_vegan": False},
    {"name": "튀김", "category": "분식", "spicy": 1, "price": 1, "allergens": ["밀", "갑각류"], "is_vegan": False},
    # 패스트푸드
    {"name": "치킨", "category": "패스트푸드", "spicy": 2, "price": 3, "allergens": ["밀"], "is_vegan": False},
    {"name": "핫도그", "category": "패스트푸드", "spicy": 1, "price": 1, "allergens": ["밀"], "is_vegan": False},
    {"name": "감자튀김", "category": "패스트푸드", "spicy": 1, "price": 1, "allergens": [], "is_vegan": True},
    # 다이어트
    {"name": "닭가슴살", "category": "다이어트", "spicy": 1, "price": 2, "allergens": [], "is_vegan": False},
    {"name": "포케", "category": "다이어트", "spicy": 1, "price": 4, "allergens": ["대두"], "is_vegan": False},
    {"name": "그릭요거트", "category": "다이어트", "spicy": 1, "price": 2, "allergens": ["우유"], "is_vegan": False},
]

# ─── 점수 계산 함수 ───
def calculate_score(menu, user_spicy, user_price, preferred_categories):
    spicy_score = 5 - abs(menu["spicy"] - user_spicy)
    price_score = 5 - abs(menu["price"] - user_price)
    total = spicy_score + price_score
    # 0~100 스케일로 변환 (최대 10점)
    return round(total / 10 * 100)

# ─── 앱 시작 ───
st.title("🍽️ 오늘 뭐 먹지?")
st.caption("맞춤 메뉴 추천 프로그램")

st.divider()

# ─── Step 1: 선호 카테고리 ───
st.subheader("Step 1 — 선호 카테고리")
categories = ["한식", "중식", "일식", "양식", "분식", "패스트푸드", "다이어트"]
selected_categories = st.multiselect(
    "좋아하는 음식 종류를 선택하세요 (복수 선택 가능)",
    categories,
    default=["한식"]
)

st.divider()

# ─── Step 2: 알레르기 / 식이제한 ───
st.subheader("Step 2 — 알레르기 / 식이제한")
allergen_options = ["갑각류", "우유", "밀", "계란", "땅콩", "대두"]
selected_allergies = st.multiselect(
    "알레르기가 있는 성분을 선택하세요",
    allergen_options,
    default=[]
)
is_vegan = st.toggle("🌱 비건 모드", value=False)

st.divider()

# ─── Step 3: 세부 선호도 ───
st.subheader("Step 3 — 세부 선호도")
user_spicy = st.slider("🌶️ 매운맛 선호도", 1, 5, 3)
user_price = st.slider("💰 가격대 선호도", 1, 5, 2,
                        help="1 = 저렴한 메뉴 선호, 5 = 비싼 메뉴도 OK")

st.divider()

# ─── Step 4: 최근 먹은 음식 ───
st.subheader("Step 4 — 최근 먹은 음식")
st.caption("선택한 메뉴는 추천에서 제외됩니다")
all_menu_names = sorted(set(m["name"] for m in menus))
recent_foods = st.multiselect(
    "최근에 먹은 음식을 선택하세요",
    all_menu_names,
    default=[]
)

st.divider()

# ─── 추천 버튼 ───
if st.button("🎯 추천 받기", type="primary", use_container_width=True):

    # 필터링
    filtered = menus.copy()

    # 0) 선호 카테고리 필터링 (선택한 카테고리의 메뉴만 추천)
    if selected_categories:
        filtered = [m for m in filtered if m["category"] in selected_categories]

    # 1) 알레르기 필터링
    if selected_allergies:
        filtered = [m for m in filtered
                    if not any(a in m["allergens"] for a in selected_allergies)]

    # 2) 비건 필터링
    if is_vegan:
        filtered = [m for m in filtered if m["is_vegan"]]

    # 3) 최근 먹은 음식 제외
    if recent_foods:
        filtered = [m for m in filtered if m["name"] not in recent_foods]

    if not filtered:
        st.warning("😢 조건에 맞는 메뉴가 없어요. 조건을 조금 완화해 보세요!")
    else:
        # 점수 계산
        scored = []
        for m in filtered:
            score = calculate_score(m, user_spicy, user_price, selected_categories)
            scored.append({**m, "score": score})

        # 점수 내림차순 정렬, 동점이면 랜덤
        scored.sort(key=lambda x: (x["score"], random.random()), reverse=True)
        top3 = scored[:3]

        st.subheader("✨ 추천 결과")

        medal = ["🥇", "🥈", "🥉"]
        card_class = ["gold", "silver", "bronze"]
        price_labels = {1: "~5,000원", 2: "~10,000원", 3: "~15,000원", 4: "~20,000원", 5: "20,000원+"}
        spicy_labels = {1: "순한맛", 2: "약간 매운맛", 3: "보통", 4: "매운맛", 5: "아주 매운맛"}

        for i, item in enumerate(top3):
            st.markdown(f"""
            <div class="result-card {card_class[i]}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <p class="menu-name">{medal[i]} {item['name']}</p>
                        <p class="menu-detail">
                            {item['category']} · {spicy_labels.get(item['spicy'], '')} · {price_labels.get(item['price'], '')}
                            {"  · 🌱 비건" if item['is_vegan'] else ""}
                        </p>
                    </div>
                    <span class="score-badge">{item['score']}점</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 필터링 요약
        with st.expander("📊 필터링 상세 정보"):
            st.write(f"전체 메뉴: **{len(menus)}개**")
            st.write(f"알레르기 필터링 후: **{len([m for m in menus if not any(a in m['allergens'] for a in selected_allergies)])}개**")
            if is_vegan:
                st.write(f"비건 필터링 후: **{len([m for m in menus if m['is_vegan']])}개**")
            st.write(f"최종 후보: **{len(filtered)}개**")
