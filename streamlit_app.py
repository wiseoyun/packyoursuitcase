import random

import streamlit as st


st.set_page_config(page_title="여행가방 무게 맞추기", page_icon="🧳")

ITEMS = {
    "book": {"name": "책", "weight": 4},
    "shirt": {"name": "티셔츠", "weight": 3},
    "pants": {"name": "바지", "weight": 5},
    "shoes": {"name": "운동화", "weight": 8},
    "towel": {"name": "수건", "weight": 2},
    "bottle": {"name": "물병", "weight": 6},
    "camera": {"name": "카메라", "weight": 7},
    "snack": {"name": "간식", "weight": 2},
    "hat": {"name": "모자", "weight": 1},
    "charger": {"name": "충전기", "weight": 2},
    "umbrella": {"name": "우산", "weight": 4},
}

CHALLENGES = [
    {"target": 12, "items": ["book", "shirt", "pants"]},
    {"target": 15, "items": ["shoes", "book", "towel", "hat"]},
    {"target": 18, "items": ["camera", "pants", "umbrella", "snack"]},
    {"target": 22, "items": ["shoes", "bottle", "book", "snack", "charger"]},
]


def format_weight(weight):
    return f"{weight // 10}.{weight % 10} kg"


if "bag_items" not in st.session_state:
    st.session_state.bag_items = []
if "challenge_index" not in st.session_state:
    st.session_state.challenge_index = 0
if "target_mode" not in st.session_state:
    st.session_state.target_mode = "문제 풀기"

st.title("🧳 여행가방 무게 맞추기")
st.write("여행 물건의 무게를 더하고 빼서 목표 무게에 맞춰 보세요!")

st.radio(
    "목표 무게 정하기",
    ["문제 풀기", "직접 목표 정하기"],
    horizontal=True,
    key="target_mode",
)

if st.session_state.target_mode == "문제 풀기":
    challenge = CHALLENGES[st.session_state.challenge_index]
    target_weight = challenge["target"]
    st.info(f"**도전 문제:** 가방 무게를 **{format_weight(target_weight)}**에 맞춰 보세요.")
    if st.button("새 문제"):
        st.session_state.challenge_index = random.randrange(len(CHALLENGES))
        st.session_state.bag_items = []
        st.rerun()
else:
    target_kg = st.number_input(
        "목표 무게 (kg)",
        min_value=0.0,
        max_value=10.0,
        value=1.5,
        step=0.1,
        format="%.1f",
    )
    target_weight = round(target_kg * 10)

st.divider()
st.subheader("여행 물건 고르기")

add_column, remove_column = st.columns(2)
item_ids = list(ITEMS)

with add_column:
    st.markdown("**가방에 넣기**")
    item_to_add = st.selectbox(
        "넣을 물건",
        item_ids,
        format_func=lambda item_id: (
            f"{ITEMS[item_id]['name']} · {format_weight(ITEMS[item_id]['weight'])}"
        ),
        label_visibility="collapsed",
        key="item_to_add",
    )
    if st.button("가방에 넣기", use_container_width=True):
        st.session_state.bag_items.append(item_to_add)

with remove_column:
    st.markdown("**가방에서 빼기**")
    if st.session_state.bag_items:
        item_to_remove = st.selectbox(
            "뺄 물건",
            range(len(st.session_state.bag_items)),
            format_func=lambda index: (
                f"{ITEMS[st.session_state.bag_items[index]]['name']} "
                f"· {format_weight(ITEMS[st.session_state.bag_items[index]]['weight'])}"
            ),
            label_visibility="collapsed",
            key="item_to_remove",
        )
        if st.button("가방에서 빼기", use_container_width=True):
            st.session_state.bag_items.pop(item_to_remove)
            st.rerun()
    else:
        st.caption("가방이 비어 있어요.")

if st.button("가방 비우기"):
    st.session_state.bag_items = []
    st.rerun()

st.divider()
st.subheader("내 여행가방")

if st.session_state.bag_items:
    for item_id in st.session_state.bag_items:
        item = ITEMS[item_id]
        st.write(f"- {item['name']} — {format_weight(item['weight'])}")
else:
    st.write("아직 가방에 물건이 없어요. 물건을 넣어 보세요.")

current_weight = sum(ITEMS[item_id]["weight"] for item_id in st.session_state.bag_items)
difference = target_weight - current_weight

weight_column, target_column, difference_column = st.columns(3)
weight_column.metric("현재 가방 무게", format_weight(current_weight))
target_column.metric("목표 무게", format_weight(target_weight))
if difference > 0:
    difference_label, difference_value = "남은 무게", format_weight(difference)
elif difference < 0:
    difference_label, difference_value = "초과한 무게", format_weight(-difference)
else:
    difference_label, difference_value = "목표와의 차이", "0.0 kg"
difference_column.metric(difference_label, difference_value)
st.progress(
    min(current_weight / target_weight, 1.0) if target_weight else int(current_weight == 0)
)

if difference == 0:
    st.success("정확히 맞췄어요! 소수의 덧셈과 뺄셈을 잘했어요!")
elif difference > 0:
    st.info(f"목표까지 **{format_weight(difference)}** 더 필요해요. 물건을 더 넣어 보세요.")
else:
    st.warning(f"목표보다 **{format_weight(-difference)}** 무거워요. 물건을 빼 보세요.")

if st.session_state.target_mode == "문제 풀기":
    with st.expander("정답 조합 보기"):
        answer_items = challenge["items"]
        answer_names = [ITEMS[item_id]["name"] for item_id in answer_items]
        st.write(" + ".join(answer_names))
        st.write(
            "무게를 더하면 "
            + " + ".join(format_weight(ITEMS[item_id]["weight"]) for item_id in answer_items)
            + f" = **{format_weight(sum(ITEMS[item_id]['weight'] for item_id in answer_items))}**"
        )
