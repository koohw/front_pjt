<script setup>
import { ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRouter } from "vue-router";
import { onMounted } from "vue";

const title = ref(null);
const content = ref(null);
const store = useCounterStore();
const router = useRouter();

const userId = computed(() => store.userProfile?.pk);

const boards = ref([
  { id: 1, name: "공지사항" },
  { id: 2, name: "자유게시판" },
  { id: 3, name: "Q&A" },
]);
const selectedBoard = ref("");
const settings = ref({
  allowComments: true,
  allowSharing: true,
  allowCopying: false,
});

// DRF로 게시글 생성 요청을 보내는 함수
const createArticle = function () {
  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/articles/`,
    data: {
      title: title.value,
      content: content.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      // console.log('게시글 작성 성공!')
      router.push({ name: "ArticleView" });
    })
    .catch((err) => {
      console.log(err);
    });
};

const profile = ref(null);

// 로그인한 사용자 정보를 가져오는 함수
const fetchUserProfile = () => {
  axios
    .get(`${store.API_URL}/api/v1/user/profile/${userId.value}`, {
      headers: {
        Authorization: `Token ${store.token}`, // 로그인 토큰을 헤더에 포함
      },
    })
    .then((response) => {
      profile.value = response.data; // 사용자 정보를 profile.value에 저장
    })
    .catch((error) => {
      console.error("사용자 정보 로드 실패:", error.response?.data);
    });
};
console.log(profile.value);

// 컴포넌트가 마운트될 때 사용자 정보를 불러옵니다.
onMounted(() => {
  fetchUserProfile();
  console.log(profile);
});
</script>

<template>
  <div class="main-container">
    <!-- 왼쪽 유저 정보 섹션 -->
    <div class="left-section">
      <div class="user-info">
        <div class="profile-icon">
          <img
            v-if="profile && profile.profile_picture"
            :src="`${store.API_URL}${profile.profile_picture}`"
            alt="유저 아이콘"
            class="profile-img"
          />
        </div>
        <div class="user-details">
          <h2>관리자</h2>
          <p>가입일: 2024.01.01</p>
        </div>
      </div>
      <div class="write-button">
        <RouterLink
          :to="{ name: 'CreateView' }"
          style="color: white; text-decoration: none"
        >
          <button style="border: none; color: white">글쓰기</button>
        </RouterLink>
      </div>
      <RouterLink :to="{ name: 'AiChatView' }" class="nav-link">
        <button class="chat-button">AI 채팅</button>
      </RouterLink>
      <div class="mypage-button">
        <RouterLink
          v-if="userId"
          :to="{ name: 'UserProfileView', params: { id: userId } }"
          style="color: white; text-decoration: none"
        >
          <button
            style="border: none; background-color: transparent; color: white"
          >
            마이 페이지
          </button>
        </RouterLink>
      </div>
    </div>

    <!-- 오른쪽 글쓰기 UI -->
    <div class="right-section">
      <div class="cafe-editor">
        <h1>커뮤니티 글쓰기</h1>
        <hr />

        <!-- 게시판 선택 및 제목 -->
        <div class="header">
          <select v-model="selectedBoard">
            <option disabled value="">게시판을 선택해 주세요.</option>
            <option v-for="board in boards" :key="board.id" :value="board.id">
              {{ board.name }}
            </option>
          </select>
          <input
            type="text"
            v-model.trim="title"
            placeholder="제목을 입력해 주세요."
          />
        </div>

        <!-- 에디터 영역 -->
        <div class="editor">
          <textarea
            v-model="content"
            placeholder="내용을 입력하세요."
          ></textarea>
        </div>

        <!-- 하단 설정 영역 -->
        <div class="settings">
          <div class="options">
            <label
              ><input type="checkbox" v-model="settings.allowComments" /> 댓글
              허용</label
            >
            <label
              ><input type="checkbox" v-model="settings.allowSharing" /> 공유
              허용</label
            >
            <label
              ><input type="checkbox" v-model="settings.allowCopying" /> 복사
              허용</label
            >
          </div>
          <button class="submit-button" @click="createArticle">등록</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");

.main-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: "NanumSquare";
  box-sizing: border-box;
}

/* 왼쪽 유저 정보 스타일 */
.left-section {
  /* flex: 1; */
  width: 300px;
  padding: 20px;
  margin-right: 20px;
  background-color: #f9f9f9;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

.user-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 20px;
  margin-top: 30px;
}

.profile-icon img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details {
  align-items: center;
  text-align: center;
}

.user-details h2 {
  font-size: 18px;
  font-weight: bold;
  margin-top: 10px;
  color: #333;
}

.user-details p {
  font-size: 15px;
  color: #555;
  margin: 5px 0;
}

.mypage-button,
.write-button,
.chat-button {
  width: 100%;
  padding: 10px;
  border: none;
  margin-bottom: 5px;
  margin-top: 5px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  text-align: center;
  background-color: #ea3e54;
}

.write-button button {
  background-color: #ea3e54;
}

.chat-button {
  background-color: #ddd;
  color: #333;
}

.mypage-button {
  background-color: #02b889;
}

/* 오른쪽 글쓰기 섹션 */
.right-section {
  flex: 4;
  padding: 40px;
  background-color: #f9f9f9;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.cafe-editor {
  max-width: 800px;
  margin-bottom: 20px;
  margin-left: 10px;
  margin-top: 10px;
  /* display: contents; */
}

h1 {
  font-family: "NanumExtraBold";
}

.header {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

header select,
header input {
  padding: 20px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.editor textarea {
  width: 100%;
  height: 300px;
  padding: 15px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: none;
}

.settings {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.options {
  display: flex;
  gap: 10px;
}

.submit-button {
  padding: 10px 20px;
  background-color: #ea3e54;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
