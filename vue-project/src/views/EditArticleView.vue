<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

const article = ref({ title: "", content: "" });

const userId = computed(() => store.userProfile?.pk);

// 게시글 데이터 가져오기
axios
  .get(`${store.API_URL}/api/v1/articles/${route.params.id}/`, {
    headers: { Authorization: `Token ${store.token}` },
  })
  .then((res) => {
    article.value = res.data;
  })
  .catch((err) => {
    console.error("게시글 조회 실패:", err.response?.data);
  });

// 수정 요청
const updateArticle = () => {
  axios
    .patch(
      `${store.API_URL}/api/v1/articles/${route.params.id}/update/`,
      article.value,
      { headers: { Authorization: `Token ${store.token}` } }
    )
    .then(() => {
      alert("게시글이 수정되었습니다.");
      router.push(`/articles/${route.params.id}`);
    })
    .catch((err) => {
      console.error("게시글 수정 실패:", err.response?.data);
    });
};

// 수정 취소
const cancleEdit = () => {
  router.push(`/articles/${route.params.id}`);
};

const currentUser = ref("");

const fetchCurrentUser = () => {
  axios
    .get(`${store.API_URL}/api/v1/current_user/`, {
      headers: { Authorization: `Token ${store.token}` },
    })
    .then((response) => {
      currentUser.value = response.data.username;
      console.log(response.data);
    })
    .catch((error) => {
      console.error("사용자 정보 로드 실패:", error.response?.data);
    });
};

onMounted(() => {
  fetchCurrentUser();
});

const profile = ref(null);

// 로그인한 사용자 정보를 가져오는 함수
const fetchUserProfile = () => {
  axios
    .get(`${store.API_URL}/api/v1/user/profile/${store.userProfile.pk}`, {
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

    <!-- 오른쪽 게시글 수정 섹션 -->
    <div class="right-section">
      <div class="cafe-update">
        <h1>게시글 수정</h1>
        <hr />
        <div class="settings">
          <form @submit.prevent="updateArticle">
            <div class="options">
              <label for="title">제목</label>
              <input id="title" v-model="article.title" required />
            </div>
            <div class="options">
              <label for="content">내용</label>
              <textarea
                id="content"
                v-model="article.content"
                required
              ></textarea>
            </div>
            <div class="button-container">
              <button class="submit-button" type="submit">저장</button>
              <button class="submit-button" @click="cancleEdit">취소</button>
            </div>
          </form>
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

/* 오른쪽 게시글 수정 섹션 */
.right-section {
  flex: 4;
  padding: 40px;
  background-color: #f9f9f9;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.cafe-update {
  max-width: 800px;
  margin: auto;
  /* margin-bottom: 20px;
  margin-left: 10px;
  margin-top: 10px; */
  display: contents;
}

.cafe-update h1 {
  font-family: "NanumExtraBold";
}

.settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
}

.settings label {
  display: block;
  font-size: 14px;
  margin-bottom: 8px;
}

.settings input,
.settings textarea {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.settings textarea {
  height: 200px;
  resize: none;
}

.options {
  gap: 10px;
}

.submit-button {
  padding: 10px 20px;
  background-color: #ea3e54;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-right: 10px;
  margin-top: 10px;
}

.submit-button:hover {
  background-color: #d0344b;
}
</style>
