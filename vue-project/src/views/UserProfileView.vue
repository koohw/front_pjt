<script setup>
import { onMounted, ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";
import axios from "axios";

const store = useCounterStore();
const router = useRouter();
const userId = store.userProfile.pk;
const profile = ref(null); // 프로필 데이터 상태
const likedMoviesDetails = ref([]); // 좋아요한 영화 상세 정보
const apiKey = import.meta.env.VITE_TMDB_API_KEY; // TMDB API 키
const baseUrl = "https://api.themoviedb.org/3"; // TMDB API URL

// 좋아요한 영화 ID 가져오기
const likedMovieIds = computed(() =>
  Object.keys(store.likedMovies).filter((key) => store.likedMovies[key])
);

// 프로필 데이터 및 좋아요한 영화 정보 가져오기
onMounted(async () => {
  try {
    // 유저 프로필 가져오기
    const response = await axios.get(
      `${store.API_URL}/api/v1/user/profile/${userId}/`
    );
    profile.value = response.data;
    console.log(profile.value);

    // 좋아요한 영화 정보 가져오기
    const moviePromises = likedMovieIds.value.map((id) =>
      axios.get(`${baseUrl}/movie/${id}`, {
        params: { api_key: apiKey, language: "ko" },
      })
    );
    const movieResponses = await Promise.all(moviePromises);
    likedMoviesDetails.value = movieResponses.map((res) => res.data);
  } catch (error) {
    console.error("데이터를 가져오는 중 오류 발생:", error);
  }
});

// 영화 세부정보 페이지 이동
const goToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetailView", params: { movieId } });
};

// 프로필 수정 페이지 이동
const goToEditPage = () => {
  router.push({ name: "EditProfileView" });
};

// 좋아요 토글
const toggleLike = async (movieId) => {
  try {
    const { liked } = await store.toggleLikeMovie(movieId);
    if (!liked) {
      likedMoviesDetails.value = likedMoviesDetails.value.filter(
        (movie) => movie.id !== movieId
      );
    }
  } catch (error) {
    console.error("좋아요 요청 실패:", error);
  }
};
</script>

<template>
  <div class="container">
    <h1>마이 페이지</h1>

    <!-- 사용자 프로필 -->
    <div v-if="profile" class="profile-container">
      <div class="profile_update">
        <img
          :src="
            `${store.API_URL}${profile.profile_picture}` ||
            'https://img.icons8.com/?size=100&id=23265&format=png'
          "
          alt="프로필 사진"
          class="profile-picture"
        />
        <button @click="goToEditPage" class="edit-button">프로필 수정</button>
      </div>

      <div class="profile_user">
        <div><strong>사용자 이름: </strong> {{ profile.username }}</div>
        <div><strong>이메일: </strong> {{ profile.email }}</div>
        <div><strong>가입일: </strong> {{ profile.join_date }}</div>
      </div>
    </div>
    <div v-else>
      <p>프로필 정보를 불러오는 중입니다...</p>
    </div>

    <!-- 좋아요한 영화 목록 -->
    <div class="favorites-container" v-if="likedMoviesDetails.length">
      <h4>관심있는 영화</h4>
      <div class="movie-list">
        <div
          v-for="movie in likedMoviesDetails"
          :key="movie.id"
          class="movie-item"
          @click="goToMovieDetail(movie.id)"
        >
          <img
            :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
            alt="포스터"
            class="movie-poster"
          />
          <button
            @click="toggleLike(movie.id)"
            style="color: transparent; border: none"
          >
            <img
              src="https://img.icons8.com/?size=100&id=19411&format=png&color=000000"
              alt="like"
            />
            {{ store.likedMovies[movie.id] }}
          </button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>관심있는 영화를 추가해보세요</p>
    </div>
  </div>
</template>

<style scoped>
@import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");

/* 전체 레이아웃 */
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: "NanumSquare";
}

/* 제목 스타일 */
h1 {
  font-size: 28px;
  font-weight: bold;
  color: #333333;
  margin-bottom: 20px;
  border-bottom: 2px solid #ececec;
  padding-bottom: 10px;
  margin-top: 10px;
  margin-left: 10px;
  font-family: "NaNumExtraBold";
}

/* 프로필 섹션 컨테이너 */
.profile-container {
  display: flex;
  align-items: center; /* 세로 정렬 중앙 */
  gap: 20px; /* 이미지와 텍스트 사이 간격 */
  margin-bottom: 20px;
}

/* 프로필 사진 */
.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
  flex-shrink: 0; /* 이미지 크기 고정 */
}

.profile_update {
  display: flex;
  flex-direction: column; /* 세로 방향 정렬 */
  margin-left: 100px;
  margin-top: 20px;
  margin-bottom: 20px;
  margin-right: 30px;
}

/* 프로필 정보 */
.profile_user {
  flex: 1; /* 나머지 공간 차지 */
  display: flex;
  flex-direction: column; /* 세로 방향 정렬 */
  align-content: center;
  gap: 10px; /* 각 정보 간 간격 */
  border: 1px solid #e5e5e5;
  padding: 50px;
  border-radius: 10px;
  margin-right: 100px;
}

.profile_user div {
  font-size: 20px;
  line-height: 1.5;
  font-family: "NanumSquare";
}

.profile_user strong {
  color: #555555;
  margin-right: 5px;
}

/* 프로필 수정 버튼 */
.edit-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #04c09e;
  color: #ffffff;
  font-size: 16px;
  text-align: center;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 20px;
  font-family: "NanumSquare";
}

.edit-button:hover {
  background-color: #02b889;
}

/* 관심 있는 영화 섹션 */
.favorites-container {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ececec;
}

h4 {
  font-size: 22px;
  font-weight: bold;
  color: #333333;
  margin-bottom: 15px;
  margin-top: 10px;
  margin-left: 10px;
  font-family: "NanumExtraBold";
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: center;
}

.movie-item {
  display: flex;
  position: relative; /* 부모 요소에 상대 위치 지정 */
  width: 220px;
  padding: 10px;
  border-radius: 10px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.movie-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.movie-poster {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 10px;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
}

button {
  padding: 0px;
  font-size: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #ff5757;
}

.movie-item button {
  position: absolute; /* 절대 위치 지정 */
  top: 17px; /* 하단에서 10px */
  right: 17px; /* 오른쪽에서 10px */
  background-color: transparent;
  cursor: pointer;
}

.movie-item button img {
  width: 40px; /* 좋아요 아이콘 크기 조정 */
  height: 40px;
  display: block;
}

.movie-item button:hover img {
  filter: brightness(2); /* 마우스 오버 시 밝기 효과 */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .profile-container {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .profile_user {
    align-items: center;
  }

  .movie-list {
    gap: 10px;
    justify-content: center;
  }

  .movie-item {
    width: 45%;
  }
}

@media (max-width: 480px) {
  .movie-item {
    width: 100%;
  }
}
</style>
