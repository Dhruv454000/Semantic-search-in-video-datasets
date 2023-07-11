<template>
  <div class="container">
    <h1 class="title">Search for videos</h1>
    <div class="input-group">
      <label for="text-desc">Text Description:</label>
      <input type="text" id="text-desc" v-model="textDesc" />
    </div>
    <div class="input-group">
      <label for="video-desc">Video Description:</label>
      <input type="text" id="video-desc" v-model="videoDesc" />
    </div>
    <div>
      <button @click="search" class="search-button">Search</button>
    </div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="results && results.length">
      <h2>Results</h2>
      <div class="card-container">
        <div v-for="(result, index) in paginatedResults" :key="index" class="card">
          <h3 class="video-id">Video ID: {{ result.video_id }}</h3>
          <p class="text">Text: {{ result.text }}</p>
          <p class="start-time">Start Time: {{ result.starttime }}</p>
          <p class="end-time">End Time: {{ result.endtime }}</p>
          <p class="metadata">Metadata: {{ result.metadata }}</p>
        </div>
      </div>
      <div class="pagination">
        <button @click="goToPreviousPage" :disabled="currentPage === 0">Previous</button>
        <button @click="goToNextPage" :disabled="currentPage === totalPages - 1">Next</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      textDesc: "",
      videoDesc: "",
      results: [],
      loading: false,
      itemsPerPage: 3, // Number of results to display per page
      currentPage: 0, // Current page index
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.results.length / this.itemsPerPage);
    },
    paginatedResults() {
      const startIndex = this.currentPage * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.results.slice(startIndex, endIndex);
    },
  },
  methods: {
    async search() {
      this.loading = true;
      try {
        const response = await axios.get("http://localhost:8000/search", {
          params: {
            text_desc: this.textDesc,
            video_desc: this.videoDesc,
          },
        });
        if (Object.prototype.hasOwnProperty.call(response.data.data.Get, "Video_text_description")) 
        {
            this.results = response.data.data.Get.Video_text_description;
        } 
        else if(Object.prototype.hasOwnProperty.call(response.data.data.Get, "Video_text"))
        {
            this.results = response.data.data.Get.Video_text;
        }
        else this.results = response.data.data.Get.Video_description; 
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    goToPreviousPage() {
      this.currentPage--;
    },
    goToNextPage() {
      this.currentPage++;
    },
  },
};
</script>

<style>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.title {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #0056b3;
}

.loading {
  text-align: center;
  margin-top: 20px;
  font-size: 16px;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  margin-top: 20px;
}

.card {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}

.video-id {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.text,
.start-time,
.end-time,
.metadata {
  margin-bottom: 10px;
}

.pagination {
  text-align: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin: 0 5px;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button:hover {
  background-color: #0056b3;
}
</style>
