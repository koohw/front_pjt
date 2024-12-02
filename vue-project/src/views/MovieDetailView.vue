<script setup>
import { useCounterStore } from "@/stores/counter";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const store = useCounterStore();
const route = useRoute();
const movieId = route.params.movieId;
const movied = route.params

const movie = ref(null);
const cast = ref([]); // 출연진 정보
const crew = ref([]); // 감독 정보
const trailerUrl = ref("");
const trailerThumbnail = ref("");
const isPlaying = ref(false); // 동영상 재생 여부

const likeCount = ref(0);

onMounted(async () => {
  const apiKey = import.meta.env.VITE_TMDB_API_KEY; // TMDB API 키
  const baseUrl = "https://api.themoviedb.org/3";
  likeCount.value = store.likedMovies[movieId] ? 1 : 0;

  try {
    // 영화 정보 가져오기
    const movieResponse = await axios.get(`${baseUrl}/movie/${movieId}`, {
      params: {
        language: "ko",
        api_key: apiKey,
      },
    });
    movie.value = movieResponse.data;

    // 출연진 및 감독 정보 가져오기
    const creditsResponse = await axios.get(`${baseUrl}/movie/${movieId}/credits`, {
      params: {
        api_key: apiKey,
        language: "ko",
      },
    });
    cast.value = creditsResponse.data.cast.slice(0, 5); // 상위 10명의 출연진만 표시
    crew.value = creditsResponse.data.crew.filter((member) => member.job === "Director"); // 감독 정보 필터링

    // 예고편 가져오기
    const youtubeResponse = await axios.get("https://www.googleapis.com/youtube/v3/search", {
      params: {
        part: "snippet",
        q: `${movie.value.original_title} Official Trailer`,
        type: "video",
        key: import.meta.env.VITE_YOUTUBE_API_KEY, // 유튜브 API 키
      },
    });
    const trailer = youtubeResponse.data.items[0];
    if (trailer) {
      trailerUrl.value = `https://www.youtube.com/watch?v=${trailer.id.videoId}`;
      trailerThumbnail.value = trailer.snippet.thumbnails.high.url;
    }
  } catch (error) {
    console.log(movied)
    console.error("Error fetching movie data:", error);
  }
});

// 동영상 재생 상태 변경
const playTrailer = () => {
  isPlaying.value = true;
};

// 좋아요 상태 토글
const toggleLike = async () => {
  try {
    const { liked } = await store.toggleLikeMovie(movieId);
    likeCount.value = liked ? likeCount.value + 1 : likeCount.value - 1;
  } catch (error) {
    console.error("좋아요 요청 실패", error);
  }
};
</script>


<template>
  <div v-if="movie" class="movieDetail">
    <div class="movieDetail__container">
      <div class="movieDetail__poster">
        <img
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          alt="movie_title"
        />
        <button @click="toggleLike" style="color:transparent; border:none;">
          <img 
            :src="store.likedMovies[movieId]
              ? 'https://img.icons8.com/?size=100&id=19411&format=png&color=000000' 
              : 'https://img.icons8.com/?size=100&id=87&format=png&color=F25081'" 
            alt="like" 
          />
          {{ store.likedMovies[movieId]}}
        </button>
      </div>
      <div class="movieDetail__info">
        <h3>{{ movie.title }}</h3>
        <p>평점: {{ movie.vote_average }}</p>
        <p>좋아요 수: {{ likeCount }}</p>
        
        <p>개봉: {{ movie.release_date }}</p>
        <p>러닝타임: {{ movie.runtime }}분</p>
        <h4>장르</h4>
        <p>
          <span v-for="genre in movie.genres" :key="genre.id" class="genre">{{
            genre.name
          }}</span>
        </p>
        <h4>줄거리</h4>
        <p>{{ movie.overview }}</p>
      </div>
    </div>

    <!-- 감독 및 출연진 섹션 -->
    <h4>감독 및 출연진</h4>
    <div class="cast-crew">
      <!-- 감독 -->
      <div v-for="director in crew" :key="director.id" class="cast-crew__member">
        <img
          :src="director.profile_path ? `https://image.tmdb.org/t/p/w200${director.profile_path}` : 'https://via.placeholder.com/200x300?text=No+Image'"
          :alt="director.name"
        />
        <p>{{ director.name }}</p>
      </div>
      <!-- 출연진 -->
      <div v-for="actor in cast" :key="actor.id" class="cast-cast__member">
        <img
          :src="actor.profile_path ? `https://image.tmdb.org/t/p/w200${actor.profile_path}` : 'https://via.placeholder.com/200x300?text=No+Image'"
          :alt="actor.name"
        />
        <p>{{ actor.name }}</p>
        <p class="character">({{ actor.character }})</p>
      </div>
    </div>


    <!-- 예고편 섹션 -->
    <h4>공식 예고편</h4>
    <div class="trailer">
      <div v-if="!isPlaying" class="trailer__thumbnail" @click="playTrailer">
        <img :src="trailerThumbnail" alt="Trailer Thumbnail" />
        <div class="play-icon">▶</div>
      </div>
      <div v-else class="trailer__video">
        <iframe
          :src="`${trailerUrl.replace('watch?v=', 'embed/')}`"
          title="Official Trailer"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>
  </div>
</template>

<style>
  @import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");
</style>

<style scoped>
.movieDetail {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.movieDetail__container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
}

.movieDetail__poster {
  position: relative;
  flex: 1;
  max-width: 300px;
}

.movieDetail__poster img {
  width: 100%;
  border-radius: 10px;
}

.movieDetail__poster button {
  position: absolute; /* 절대 위치 지정 */
  top: 7px;
  right: 7px;
  background-color: transparent;
  cursor: pointer;
}

.movieDetail__poster button img {
  width: 60px; /* 좋아요 아이콘 크기 조정 */
  height: 60px;
  display: block;
}

.movieDetail__poster button:hover img {
  filter: brightness(2.0); /* 마우스 오버 시 밝기 효과 */
}

.movieDetail__info {
  flex: 2;
  margin-left: 20px;
}

h3,
h4 {
  color: black;
  font-weight: bold;
  margin-bottom: 10px;
  font-family: 'NanumSquareExtraBold';
  border-radius: 10px;

}

p {
  color: #333;
  margin: 5px 0;
  font-family: 'NanumSquareAcr';

}

.genre {
  padding: 7px;
  display: inline-block;
  margin: 5px;
  background-color: #f0f0f0;
  border-radius: 5px;
  font-family: 'NanumSquareAcb';

}

.trailer {
  margin-top: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center; /* 컨텐츠를 중앙에 정렬 */
}

.trailer__thumbnail {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.trailer__thumbnail img {
  width: 100%;
  max-width: 640px;
  border-radius: 10px;
}

.trailer__thumbnail .play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 50px;
  color: red;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  border: none; /* 테두리 제거 */
}

.trailer__video iframe {
  width: 100%;
  max-width: 640px;
  height: 360px;
  border-radius: 10px;
}

.cast-crew {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.cast-crew__member,
.cast-cast__member {
  text-align: center;
  width: 150px;
}

.cast-crew__member img,
.cast-cast__member img {
  width: 100%;
  border-radius: 10px;
}

.character {
  font-size: 14px;
  color: gray;
}
</style>
