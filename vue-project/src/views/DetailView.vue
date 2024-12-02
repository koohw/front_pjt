<script setup>
import axios from "axios";
import { onMounted, ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

// Article 및 댓글 관련 데이터
const article = ref(null);
const comments = ref([]); // 댓글 목록
const newComment = ref("");

const userId = computed(() => store.userProfile?.pk);

// 댓글 작성 함수
// profile을 ref로 선언하여 사용자 정보를 저장
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

// 컴포넌트가 마운트될 때 사용자 정보를 불러옵니다.
onMounted(() => {
  fetchUserProfile();
  console.log(profile);
});

// 게시글 및 댓글 조회
onMounted(() => {
  // 게시글 조회
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`, // 로그인 토큰을 헤더에 추가
    },
  })
    .then((res) => {
      // console.log("게시글 응답 데이터:", res.data); // 게시글 데이터 로그
      article.value = res.data;
    })
    .catch((err) => {
      console.log("게시글 조회 오류:", err);
      console.log(route.params.id);
    });

  // 댓글 조회
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`, // 로그인 토큰을 헤더에 추가
    },
  })
    .then((res) => {
      console.log("댓글 응답 데이터:", res.data); // 댓글 데이터 로그
      comments.value = res.data;
    })
    .catch((err) => {
      console.log("댓글 조회 오류:", err);
      console.log(route.params.id);
    });
});

const postComment = () => {
  if (!newComment.value.trim()) {
    alert("댓글을 입력해주세요.");
    return;
  }

  const requestData = {
    content: newComment.value.trim(), // content만 포함
  };

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/comments/`,
    data: requestData,
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      comments.value.unshift(response.data); // 댓글 목록에 새 댓글 추가
      newComment.value = ""; // 입력 필드 초기화
    })
    .catch((error) => {
      console.error("댓글 작성 실패:", error.response?.data);
      alert("댓글 작성에 실패했습니다. 다시 시도해주세요.");
    });
};

const deleteComment = (commentId) => {
  if (!confirm("정말로 댓글을 삭제하시겠습니까?")) {
    return;
  }

  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      // 댓글 목록에서 삭제된 댓글 제거
      comments.value = comments.value.filter(
        (comment) => comment.id !== commentId
      );
      alert("댓글이 삭제되었습니다.");
    })
    .catch((error) => {
      console.error("댓글 삭제 실패:", error.response?.data);
      alert("댓글 삭제에 실패했습니다.");
    });
};

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
    });
};

onMounted(() => {
  fetchCurrentUser();
});

// 게시글 삭제
const deleteArticle = () => {
  if (!confirm("정말로 게시글을 삭제하시겠습니까?")) {
    return;
  }

  axios
    .delete(`${store.API_URL}/api/v1/articles/${route.params.id}/delete/`, {
      headers: { Authorization: `Token ${store.token}` },
    })
    .then(() => {
      alert("게시글이 삭제되었습니다.");
      // Vue 상태에서 게시글 삭제
      router.push("/articles");
    })
    .catch((err) => {
      console.error("게시글 삭제 실패:", err.response?.data);
    });
};

const goToEditPage = () => {
  router.push(`/articles/${article.value.id}/edit`);
};

const goToCreatePage = () => {
  router.push(`/articles/create`);
};
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

    <!-- 게시글 디테일 -->
    <div class="right-section">
      <div v-if="article" class="article-detail">
        <h1>{{ article.title }}</h1>
        <p>
          <img
            style="width: 30px; margin-right: 5px"
            src="https://img.icons8.com/?size=100&id=65342&format=png&color=000000"
            alt="작성자 아이콘"
            class="user-icon"
          />{{ article.user }}
        </p>
        <p>{{ article.created_at }}</p>
        <hr />
        <h2>{{ article.content }}</h2>
        <!-- 디버깅 용 -->
        <!-- <div>
          <p>현재 사용자: {{ currentUser }}</p>
          <p>작성자: {{ article?.user }}</p>
          <p>작성자: {{ article.id }}</p>
        </div> -->
      </div>
      <div v-else>
        <p>게시글을 불러오는 중입니다...</p>
      </div>
      <div></div>

      <!-- 댓글 목록 -->
      <div v-if="comments.length > 0">
        <h5>등록순</h5>
        <ul>
          <li v-for="comment in comments" :key="comment.id">
            <p>
              <img
                style="width: 29px; margin-right: 5px"
                src="https://img.icons8.com/?size=100&id=65342&format=png&color=000000"
                alt="댓글 작성자 아이콘"
                class="user-icon"
              /><strong>{{ comment.user }} </strong> <br />{{ comment.content }}
            </p>
            <!-- 작성자만 삭제 버튼 표시 -->
            <button
              class="manage-button"
              v-if="comment.user === currentUser"
              @click="deleteComment(comment.id)"
            >
              <img
                src="https://img.icons8.com/?size=100&id=102350&format=png&color=000000"
                alt="삭제 아이콘"
                class="icon"
              />
            </button>
          </li>
        </ul>
      </div>

      <!-- 댓글 작성 폼 -->
      <div v-if="store.isLogin">
        <textarea
          v-model="newComment"
          placeholder="댓글을 작성하세요"
          rows="4"
        ></textarea>
        <button
          class="manage-button"
          style="background-color: #ea3e54; margin-left: 10px"
          @click="postComment"
        >
          등록
        </button>
      </div>
      <div v-else>
        <p>로그인 후 댓글을 작성할 수 있습니다.</p>
      </div>
      <hr />
      <div class="change" v-if="article && currentUser === article.user">
        <button class="manage-button" style="background-color: #ea3e54">
          <RouterLink
            :to="{ name: 'CreateView' }"
            style="color: white; text-decoration: none"
          >
            <img
              style="width: 20px"
              src="https://img.icons8.com/?size=100&id=11737&format=png&color=FFFFFF"
              alt=""
            />
            글쓰기
          </RouterLink>
        </button>
        <button class="manage-button" @click="goToEditPage">수정</button>
        <button class="manage-button" @click="deleteArticle">삭제</button>
      </div>
    </div>
  </div>
</template>

<style>
@import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");
</style>

<style scoped>
/* 게시글 스타일 */
/* 전체를 감싸는 컨테이너 */
.main-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  max-width: 1500px;
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

/* 오른쪽 게시글 스타일 */
.right-section {
  flex: 4;
  padding: 40px;
  background-color: #f9f9f9;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

h1 {
  font-size: 40px;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-top: 25px;
  font-family: "NanumExtraBold";
}

.article-detail h2 {
  margin-bottom: 20px;
  margin-left: 20px;
  margin-top: 25px;
  font-family: "NanumSquare";
}

.change {
  display: flex;
  justify-content: flex-start;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  gap: 10px;
  font-family: "NanumBold";
}

.change button {
  background-color: lightgrey;
}

.change button:hover {
  background-color: #d23a4a; /* hover 시 색상 변경 */
}

/* 댓글 목록 */
h5 {
  font-size: 18px;
  color: #0073e6;
  cursor: pointer;
  text-decoration: underline;
}

p {
  margin-top: 5px;
  margin-left: 20px;
  font-size: 15px;
}

div[v-if="article"] {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
  background-color: #f9f9f9;
  margin-bottom: 20px;
}

/* 댓글 목록 스타일 */
h5 {
  margin-top: 50px;
  margin-bottom: -300px;
  display: inline-block;
  font-size: 18px;
  margin-left: 20px;
  color: #0073e6;
  cursor: pointer;
  text-decoration: underline;
}

ul {
  list-style: none;
  padding: 0;
}
li {
  border-bottom: 1px solid #ddd;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

li p {
  font-size: 18px;
  color: #555;
}

li button img {
  width: 25px;
  height: 25px;
  vertical-align: middle;
  background: transparent; /* 투명한 배경 */
}

/* 댓글 작성 폼 */
textarea {
  width: 90%;
  padding: 10px;
  margin-top: 10px;
  margin-left: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  font-size: 14px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.manage-button {
  /* background-color: white; */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  background: transparent;
}

.manage-button:hover {
  background-color: transparent;
}

/* 로그인 안내 문구 */
div[v-else] {
  margin-top: 20px;
  font-size: 14px;
  color: #999;
  text-align: center;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  div {
    padding: 10px;
  }

  h1 {
    font-size: 24px;
  }

  h2 {
    font-size: 20px;
  }

  p {
    font-size: 14px;
  }

  button {
    font-size: 14px;
  }

  li {
    flex-direction: column;
    align-items: flex-start;
  }

  li button {
    margin-top: 5px;
  }
}
</style>
