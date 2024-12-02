<template>
  <div>
    <ul>
      <li>
        <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" style="text-decoration: none;">
          <div class="container">
            <h5>{{ article.title }}</h5>
          </div>
        </RouterLink>
      </li>
    </ul>
    <hr />
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

defineProps({
  article: Object,
});
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  border-radius: 4px;
  background-color: #fafafa;
  transition: background-color 0.3s;
}

.container:hover {
  background-color: #f0f0f0; /* hover 시 배경 색상 변경 */
}

h5 {
  color: #555;
  margin: 0;
  /* text-decoration: none; */
}

.article-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.container:focus-within {
  outline: none;
}
</style>