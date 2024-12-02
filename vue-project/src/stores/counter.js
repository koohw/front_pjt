import axios from "axios";
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore(
  "counter",
  () => {
    const articles = ref([]);
    const API_URL = "http://127.0.0.1:8000";
    const token = ref(localStorage.getItem("token")); // localStorage에서 token을 가져옴
    const movies = ref([]);
    const router = useRouter();
    
    
    // 유저 정보 상태
    const userProfile = ref({});  // 유저 정보 저장 상태
    const user = ref({}); // 유저 정보 저장 상태
    const likedMovies = ref({}); // 좋아요 상태 저장 (영화 ID별로)
    
    // 로그인 상태 여부 (token이 있으면 true, 없으면 false)
    const isLogin = computed(() => !!token.value); 

    // 회원가입
    const signUp = function (payload) {
      const { username, password1, password2 } = payload;

      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          password1,
          password2,
        },
      })
        .then((res) => {
          alert("회원가입이 완료되었습니다.");
          router.push({ name: "LogInView" }); // LoginView로 이동
        })
        .catch((err) => {
          if (err.response && err.response.data) {
            const errors = err.response.data;
            let errorMessages = "";
            for (const field in errors) {
              if (errors[field] && Array.isArray(errors[field])) {
                errorMessages += `${field} 오류: ${errors[field].join(", ")}\n`;
              }
            }

            if (errorMessages) {
              alert(errorMessages); // 오류 메시지 경고창
            } else {
              alert("알 수 없는 오류가 발생했습니다.");
            }
          } else {
            alert("서버와 통신에 실패했습니다.");
          }
        });
    };

    // 로그인
    const logIn = function (payload) {
      const { username, password } = payload;

      if (token.value) {
        alert("이미 로그인 되어있습니다.");
        return;
      }

      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          token.value = res.data.key; // 로그인 후 토큰 저장
          localStorage.setItem("token", res.data.key); // 토큰을 localStorage에 저장

          // 로그인 후 유저 정보를 가져오기 위해 토큰을 사용하여 유저 정보 요청
          return axios({
            method: "get",
            url: `${API_URL}/accounts/user/`,
            headers: {
              Authorization: `Token ${token.value}`,
            },
          });
        })
        .then((res) => {
          user.value = res.data; // 유저 정보를 `user`에 저장
          userProfile.value = res.data; // userProfile에도 저장 (마이페이지에서 사용)
          router.push({ name: "HomeView" }); // 로그인 후 ArticleView로 이동
        })
        .catch((err) => {
          if (err.response && err.response.status === 400) {
            alert("회원정보가 없거나 잘못된 정보입니다. 회원가입을 해주세요.");
            router.push({ name: "SignUpView" });
          } else {
            console.log(err); // 기타 에러 처리
          }
        });
    };

    // 로그아웃 요청 액션
    const logOut = async () => {
      if (!token.value) {
        alert("로그인 상태가 아닙니다.");
        router.push({ name: "LogInView" });
        return;
      }

      try {
        // 서버 로그아웃 요청
        await axios({
          method: "post",
          url: `${API_URL}/accounts/logout/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });

        // 클라이언트 상태 초기화
        token.value = null;
        userProfile.value = {}; // 로그아웃 시 userProfile 초기화
        user.value = {}; // 로그아웃 시 user 정보 초기화
        localStorage.removeItem("token"); // localStorage에서 토큰 삭제
        alert("로그아웃 되었습니다.");
        router.push({ name: "LogInView" }); // 로그아웃 후 로그인 페이지로 이동
      } catch (err) {
        console.error("로그아웃 요청 실패:", err);
        if (err.response?.status === 401) {
          alert("인증 정보가 유효하지 않습니다. 다시 로그인하세요.");
          token.value = null;
          userProfile.value = {}; // userProfile 초기화
          user.value = {}; // user 정보 초기화
          localStorage.removeItem("token");
          router.push({ name: "LogInView" });
        } else {
          alert("로그아웃에 실패했습니다. 다시 시도해주세요.");
        }
      }
    };

    // 유저 정보 가져오기
    const getUserProfile = () => {
      if (!token.value) {
        alert("로그인 후에 정보를 조회할 수 있습니다.");
        return;
      }
    
      axios({
        method: "get",
        url: `${API_URL}/accounts/user/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((response) => {
          userProfile.value = response.data; // 유저 프로필 저장
          user.value = response.data; // user 정보 저장
          console.log(response.data)
        })
        .catch((err) => {
          console.error("유저 정보를 가져오는 데 실패했습니다.", err);
          alert("유저 정보를 가져오는 데 실패했습니다.");
        });
    };
    console.log(user)
    

    // 프로필 업데이트
    const updateUserProfile = async (payload) => {
      if (!token.value) {
        alert("로그인 후에 프로필을 수정할 수 있습니다.");
        return;
      }

      try {
        const response = await axios({
          method: "put",
          url: `${API_URL}api/v1/user/profile/${userProfile.value.id}/update/`,
          data: payload,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });

        userProfile.value = response.data;  // 수정된 프로필 정보를 상태에 저장
        user.value = response.data;  // user 정보도 업데이트
        alert("프로필이 업데이트되었습니다.");
      } catch (err) {
        console.error("프로필 업데이트에 실패했습니다.", err);
        alert("프로필 업데이트에 실패했습니다.");
      }
    };

    // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          articles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    // 영화 데이터 가져오기
    const getMovies = () => {
      const apikey = import.meta.env.VITE_TMDB_API_KEY;
      axios
        .get(
          `https://api.themoviedb.org/3/movie/top_rated?api_key=${apikey}&language=ko-KR&page=1`
        )
        .then((response) => {
          movies.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };


    // 영화 좋아요 토글
    const toggleLikeMovie = async (movieId) => {
      if (!isLogin.value) {
        alert("로그인 후 좋아요를 사용할 수 있습니다.");
        router.push({ name: "LogInView" });
        return;
      }

      try {
        const response = await axios.post(
          `${API_URL}/api/v1/movies/${movieId}/like/`,
          {}, // Body 없이 POST 요청
          {
            headers: {
              Authorization: `Token ${token.value}`, // 인증 토큰 추가
            },
          }
        );

        // 좋아요 상태 업데이트
        likedMovies.value[movieId] = response.data.liked; // 서버 응답에서 liked 상태 가져옴
        return response.data;
      } catch (error) {
        console.error("좋아요 토글에 실패했습니다.", error);
        alert("좋아요 요청 중 오류가 발생했습니다.");
        throw error;
      }
    };

    // 특정 영화의 좋아요 상태 확인
    const isMovieLiked = (movieId) => {
      return !!likedMovies.value[movieId];
    };

    // `signUp`을 반환된 객체에 포함시킴
    return {
      articles,
      API_URL,
      getArticles,
      signUp, // signUp 함수 포함
      logIn,
      token,
      isLogin,
      logOut,
      movies,
      getMovies,
      userProfile,
      getUserProfile,
      updateUserProfile,
      likedMovies,
      toggleLikeMovie,
      isMovieLiked,
    };
  },
  { persist: true } // Pinia 상태를 브라우저에 유지
);
