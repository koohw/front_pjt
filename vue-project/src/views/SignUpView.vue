<template>
  <br>
  <br>
  <br>
  <div class="signup-container">
    <h1>회원가입</h1>
    <p>아래 정보를 입력하고 계정을 생성하세요.</p>
    <form @submit.prevent="signUp" class="signup-form">
      <div class="form-group">
        <label for="username" style="margin-right:10px;">아이디</label>
        <input type="text" id="username" v-model.trim="username" placeholder="아이디를 입력하세요" required>
      </div>

      <div class="form-group">
        <label for="password1" style="margin-right:10px;">비밀번호</label>
        <input type="password" id="password1" v-model.trim="password1" placeholder="비밀번호를 입력하세요" required>
      </div>

      <div class="form-group">
        <label for="password2" style="margin-right:10px;">비밀번호 확인</label>
        <input type="password" id="password2" v-model.trim="password2" placeholder="비밀번호를 다시 입력하세요" required>
      </div>

      <button type="submit" class="submit-button">회원가입</button>
    </form>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const store = useCounterStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}

</script>

<style>
  @import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");
</style>

<style scoped>
/* 전체 컨테이너 스타일 */
.signup-container {
  border: 1px;
  max-width: 600px;
  height: 380px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  text-align: center;
}

/* 헤더 스타일 */
.signup-container h1 {
  font-size: 24px;
  font-weight: bold;
  color: #333333;
  margin-bottom: 10px;
  font-family: "NanumExtraBold",
}

.signup-container p {
  font-size: 14px;
  color: #666666;
  margin-bottom: 20px;
}

/* 폼 스타일 */
.signup-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  font-family: "NanumSquare";
  background-color: white;
  
}

/* 입력 필드 스타일 */
.form-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: "NanumSquare";
}

.form-group label {
  margin-left: 20px;
}

/* 입력 필드 스타일 */
.form-group input {
  width: 100%;
  max-width: 400px;
  padding: 12px 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 20px; /* 둥근 테두리 */
  outline: none;
  transition: border-color 0.3s ease;
  margin-right: 20px;
}

/* 입력 필드 포커스 시 효과 */
.form-group input:focus {
  border-color: #ea3e54;
  box-shadow: 0 0 5px rgba(234, 62, 84, 0.5);
}

/* 입력 필드 안의 placeholder 스타일 */
.form-group input::placeholder {
  color: #bbb;
  font-size: 14px;
}

.submit-button {
  margin-top: 10px;
  width: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;  /* 투명한 배경 */
  border-radius: 20px;
  margin-left: 90px;
  background-color: #ea3e54;
  color: white;
  border: none;
  font-family: "NanumExtraBold";
  padding: 12px 0;
  font-size: 16px;
  cursor: pointer;
}

/* 버튼 hover 효과 */
.submit-button:hover {
  background-color: #c73145;
}
</style>