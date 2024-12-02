<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";
import axios from "axios";

const store = useCounterStore();
const router = useRouter();

// userProfile을 ref로 정의하여 템플릿에서 사용
const userProfile = ref(store.userProfile); // store에서 userProfile을 가져옴
const userId = store.userProfile ? store.userProfile.pk : null; // userId는 userProfile이 있을 때만 설정

const formData = ref({
  username: "",
  email: "",
  password: "",
  bio: "",
  address: "",
  profile_picture: null,
});

const fetchUserProfile = () => {
  if (userId) {
    axios
      .get(`${store.API_URL}/api/v1/user/profile/${userId}`, {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      })
      .then((response) => {
        formData.value = { ...response.data, password: "" };
      })
      .catch((error) => {
        console.error("사용자 정보 로드 실패:", error.response?.data);
      });
  }
};

onMounted(() => {
  if (userId) {
    fetchUserProfile();
  }
});

const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    formData.value.profile_picture = file;
  }
};

const updateProfile = async () => {
  const updatedData = new FormData();

  updatedData.append("username", formData.value.username || "");
  updatedData.append("email", formData.value.email || "");
  updatedData.append("password", formData.value.password || "");
  updatedData.append("bio", formData.value.bio || "");
  updatedData.append("address", formData.value.address || "");
  if (formData.value.profile_picture) {
    updatedData.append("profile_picture", formData.value.profile_picture);
  }

  axios({
    method: "put",
    url: `${store.API_URL}/api/v1/user/profile/${userId}/update/`,
    data: updatedData,
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "multipart/form-data",
    },
  })
    .then(() => {
      alert("프로필이 성공적으로 수정되었습니다!");
      router.push({ name: "UserProfileView", params: { id: userId } });
    })
    .catch((error) => {
      console.error("프로필 수정 실패:", error.response?.data);
    });
};
</script>

<template>
  <div class="container">
    <h1>회원정보 수정</h1>

    <!-- userProfile이 null이 아니면 프로필 수정 폼 렌더링 -->
    <div v-if="userProfile">
      <div class="profile-container">
        <div class="profile-picture-container">
          <!-- 기존 사진이 있으면 그것을 렌더링하고 없으면 기본 이미지를 렌더링 -->
          <img
                v-if="typeof formData.profile_picture === 'string'"
                :src="formData.profile_picture"
                alt="프로필 사진"
                class="profile-picture"
            />

          <img
            v-else
            src="https://img.icons8.com/?size=100&id=23265&format=png"
            alt="기본 프로필 사진"
            class="profile-picture"
          />
          <input
            type="file"
            accept="image/*"
            @change="handleFileChange"
            class="profile-picture-input"
          />
        </div>

        <form @submit.prevent="updateProfile" class="form-container">
          <div>
            <label for="username">사용자 이름</label>
            <input
              type="text"
              v-model="formData.username"
              id="username"
              required
            />
          </div>
          <div>
            <label for="email">이메일</label>
            <input type="email" v-model="formData.email" id="email" required />
          </div>

          <!-- 비밀번호 수정 필드 추가 (옵션) -->
          <div>
            <label for="password">새 비밀번호</label>
            <input type="password" v-model="formData.password" id="password" />
          </div>

          <button type="submit" class="submit-button">프로필 수정</button>
        </form>
      </div>
    </div>

    <div v-else>
      <p>프로필 정보를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<style scoped>
@import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");

.container {
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
  background-color: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: "NanumSquare";
}

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

.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.profile-picture-container {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
}

.profile-picture {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.profile-picture-input {
  margin-top: 10px;
  cursor: pointer;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
  width: 80%;
}

label {
  font-size: 16px;
  font-weight: bold;
  font-family: "NanumSquare";
  display: inline-block;
  width: 80%;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  font-size: 14px;
  border-radius: 4px;
  border: 1px solid #ddd;
  font-family: "NanumSquare";
  width: 100%;
  max-width: 500px;
}

.submit-button {
  padding: 10px;
  background-color: #ea3e54;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-family: "NanumSquare";
  width: 100%;
  margin-top: 10px;
}

.submit-button:hover {
  background-color: #d23a4a;
}
</style>
