<template>
  <div class="container">
    <h1>Search</h1>
    <div>
      <label for="text-desc">Text Description:</label>
      <input type="text" id="text-desc" v-model="textDesc" />
    </div>
    <div>
      <label for="video-desc">Video Description:</label>
      <input type="text" id="video-desc" v-model="videoDesc" />
    </div>
    <div>
      <button @click="search">Search</button>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-if="results.length">
      <h2>Results</h2>
      <ul>
        <li v-for="(result, index) in results" :key="index">
          <h3>Video ID: {{ result.video_id }}</h3>
          <p>Text: {{ result.text }}</p>
          <p>Start Time: {{ result.starttime }}</p>
          <p>End Time: {{ result.endtime }}</p>
          <p>Metadata: {{ result.metadata }}</p>
        </li>
      </ul>
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
    };
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
        this.results = response.data.data.Get.Video_text_description;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
  },
  watch: {
    results: {
      handler() {
        this.$nextTick(() => {
          // Additional view-related operations if needed
        });
      },
      deep: true,
    },
  },
};
</script>

<style>
.container {
  max-width: 600px;
  margin: 0 auto;
}
</style>
