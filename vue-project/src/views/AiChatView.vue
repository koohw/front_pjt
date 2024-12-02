<template>
  <h1>영화 여행, 그 곳을 알려드립니다.</h1>
  <h4>영화에서 본 그 멋진 장소, 이제 현실로 만날 수 있습니다!</h4>
  <div class="search-container">
    <!-- 검색창 -->
    <div class="input-container">
      <input
        type="text"
        v-model="query"
        placeholder="영화 장면의 장소에 대해 물어보세요"
        @keydown.enter="handleSearch"
        class="search-input"
      />
      <button @click="handleSearch" class="search-btn">검색</button>
    </div>

    <!-- 로딩 중 표시 (스피너) -->
    <div v-if="loading" class="loading-container">
      <div class="loading-percent">{{ loadingPercent }}%</div>
      <div class="spinner"></div>
    </div>
    
    <div class="results-res">

      <!-- 검색 결과 -->
      <div v-if="!loading && results.length > 0" class="results-container">
        <div v-for="(result, index) in results" :key="index" class="result">
          <h3>{{ result.title }}</h3>
          <p>{{ result.description }}</p>
        </div>
      </div>

      <!-- 지도 -->
      <div v-if="location" id="map"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// 검색 입력 상태
const query = ref("");
const loading = ref(false);
const loadingPercent = ref(0);
const results = ref([]); // 검색 결과
const location = ref(null); // 위치 정보

// Google Maps API Key
const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

// 로딩 퍼센트 증가
// 로딩 퍼센트 증가
const startLoading = () => {
  loading.value = true;
  loadingPercent.value = 0;

  const interval = setInterval(() => {
    if (loading.value && loadingPercent.value < 99) {
      loadingPercent.value += 1; // 99%까지 증가
    } else {
      clearInterval(interval); // 로딩이 완료되면 정지
    }
  }, 50); // 50ms마다 1%씩 증가
};

// 로딩 종료
const stopLoading = () => {
  loading.value = false;
  loadingPercent.value = 0;
};

// 지도 로드
const loadGoogleMaps = () => {
  const script = document.createElement("script");
  script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&callback=initMap`;
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
};

const initMap = () => {
  if (!location.value) return;

  const { lat, lng } = location.value;
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat, lng },
    zoom: 13,
  });

  new google.maps.Marker({
    position: { lat, lng },
    map,
    title: "영화 장면의 장소",
  });
};

window.initMap = initMap;

// 검색 처리
const handleSearch = async () => {
  if (query.value.trim() === "") return;

  // 로딩 시작
  startLoading();

  try {
    // 사용자 입력을 기반으로 검색
    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `당신은 영화와 여행을 좋아하는 평론가 영화 장면 속 장소들도 많이 가보았고 그 영화가 어느 장소가 유명하지인지 알고 있습니다. 저에게 영화와 영화 속 장소에 대해 알려주세요. 다음과 같은 정보를 포함해 주세요:
                          1. 영화 제목
                          2. 영화 속 장소 (국가, 도시, 장소 등)
                          3. 그 장소에서 촬영된 영화 장면의 설명
                          4. 그 장소에 대한 설명 (역사적 배경, 유명한 이유 등)
                          5. 해당 장소의 위도와 경도
                          영화 제목과 장면의 장소, 해당 장소에서의 영화 장면 설명과 장소 설명, 위도, 경도를 포함하여 응답해주세요. 
                          예:영화 제목: [영화 제목],
                            장소: [국가, 도시, 장소],
                            장소에서의 영화 정보 설명: [장소에서 촬영된 영화 내용],
                            위도: [위도],
                            경도: [경도]
                            예시에서 ',' 는 엔터 치고 답변을 내줘`,
          },
          { role: "user", content: query.value },
        ],
      },
      {
        headers: {
          Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    const botMessage = response.data.choices[0].message.content;
    const locationRegex = /위도\s*[:：]?\s*(-?\d+\.\d+)[,\s]+경도\s*[:：]?\s*(-?\d+\.\d+)/;
    const locationMatch = botMessage.match(locationRegex);

    // 결과 처리
    results.value = [
      {
        title: "영화 장면 위치",
        description: botMessage,
      },
    ];

    if (locationMatch) {
      location.value = {
        lat: parseFloat(locationMatch[1]),
        lng: parseFloat(locationMatch[2]),
      };
      loadGoogleMaps(); // 지도 로드
    }

  } catch (error) {
    console.error("검색 실패:", error);
  } finally {
    stopLoading();
  }
};
</script>

<style scoped>
@import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");

h1 {
  font-family: 'NanumSquareAcr';
  margin-left: 45px;
  display: flex;
  justify-content: center;
  align-items: center;
}

h4 {
  font-family: 'NanumSquareAcr';
  margin-left: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
}
/* 전체 컨테이너 스타일 */
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'NanumSquareAcr';
  display: flex;
  flex-direction: column; /* 요소를 세로로 배열 */
  justify-content: center;
  align-items: center;
  gap: 20px; /* 요소 간격 */
}

/* 검색 결과와 지도 컨테이너 */
.results-res {
  display: flex;
  flex-direction: column; /* 세로 배열 */
  gap: 20px; /* 요소 간 간격 */
  width: 100%; /* 가로 길이 조정 */
}

.results-container {
  width: 100%; /* 가로를 검색창에 맞춤 */
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

#map {
  /* width: 100%; 지도도 가로를 검색창에 맞춤 */
  height: 500px;
  background-color: #eaeaea;
}

/* 검색창 스타일 */
.input-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%; /* 검색창의 가로 크기 조정 */
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  margin-right: 10px; /* 버튼과의 간격 */
}

.search-btn {
  background-color: #ea3e54;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-btn:hover {
  filter: brightness(2.0);
}
</style>