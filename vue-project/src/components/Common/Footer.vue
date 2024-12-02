<template>
    <footer class="footer">
      <div class="footer-content">
        <p>
            <a href="https://www.themoviedb.org/" target="_blank" rel="noopener noreferrer">
                Powered by TMDB
            </a>
        </p>  
      </div>
    </footer>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  // 현재 연도를 계산
  </script>
  
  <style scoped>
  @import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");
  
  .footer {
    background-color: transparent;
    color: white;
    padding: 20px 0;
    text-align: center;
    font-family: 'NanumSquareAcr', sans-serif;
    position: relative;
    bottom: -30px;
    width: 100%;
  }
  
  .footer-content p {
    margin: 5px 0;
  }
  
  .footer-content a {
    color: #ea3e54;
    text-decoration: none;
    font-weight: bold;
  }
  
  .footer-content a:hover {
    text-decoration: underline;
  }
  </style>
  