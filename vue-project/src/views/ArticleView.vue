<script setup>
import axios from "axios";
import ArticleList from "@/components/ArticleList.vue";
import { onMounted, ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import { RouterLink } from "vue-router";

const userId = computed(() => store.userProfile?.pk);

const store = useCounterStore();

onMounted(() => {
  // mount 되기 전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles();
});

// 사용자 정보 로드
const currentUser = ref("");
const fetchCurrentUser = () => {
  axios
    .get(`${store.API_URL}/api/v1/current_user/`, {
      headers: { Authorization: `Token ${store.token}` },
    })
    .then((response) => {
      currentUser.value = response.data.username;
    })
    .catch((error) => {
      console.error("사용자 정보 로드 실패:", error.response?.data);
      console.log(store.token);
    });
};

onMounted(() => {
  fetchCurrentUser();
});
console.log(userId);
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
console.log(store);

// 컴포넌트가 마운트될 때 사용자 정보를 불러옵니다.
onMounted(() => {
  fetchUserProfile();
  console.log(profile);
  console.log(userId.value);
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
          <h2>{{ currentUser }}</h2>
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

    <!-- 오른쪽 게시글 섹션 -->
    <div class="right-section">
      <div class="article-section">
        <h1>전체 글 보기</h1>
        <hr style="height: 5px" />
        <ArticleList />
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
  max-width: 1500px;
  margin: 0 auto; /* 화면 중앙 정렬 */
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

/* 오른쪽 게시글 스타일 */
.right-section {
  flex: 4;
  padding: 40px;
  background-color: #f9f9f9;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.article-section {
  /* font-size: 40px; */
  margin-bottom: 20px;
  margin-left: 10px;
  margin-top: 10px;
  font-family: "NanumSquare";
}

.article-section h1 {
  font-family: "NanumExtraBold";
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }
  .left-section {
    margin-right: 0;
    margin-bottom: 20px;
  }
}
</style>
