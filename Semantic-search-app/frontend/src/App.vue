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
   <div class="input-group">
    <label for="no-of-records">No of Records:</label>
    <input type="number" id="no-of-records" v-model="noOfRecords" @focus="showNoOfRecordsTooltip = true" @input="showNoOfRecordsTooltip = false" />
    <div class="tooltip" v-if="showNoOfRecordsTooltip">Enter the number of records you want.</div>
  </div>

  <div class="input-group">
    <label for="minimum-distance">Minimum Distance:</label>
    <input type="number" id="minimum-distance" v-model="minimumDistance" @focus="showMinimumDistanceTooltip = true" @input="showMinimumDistanceTooltip = false" />
    <div class="tooltip" v-if="showMinimumDistanceTooltip">Enter distance between (0,1]. More closer to 0 means better results.</div>
  </div>
    <div>
      <button @click="search" class="search-button">Search</button>
      <button @click="downloadCSV" class="download-button">Download CSV</button>
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
          <p class="additional-info">Distance: {{ result._additional.distance }}</p>
          <p class="additional-info">Video Link: {{ generateVideoLink(result.video_id, result.starttime, result.endtime) }}</p>
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
import { saveAs } from "file-saver";

export default {
  data() {
    return {
      textDesc: "",
      videoDesc: "",
      noOfRecords: 1,
      minimumDistance: 1,
      results: [],
      loading: false,
      itemsPerPage: 3, // Number of results to display per page
      currentPage: 0, // Current page index
      showNoOfRecordsTooltip: false,
      showMinimumDistanceTooltip: false,
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
            n_records: this.noOfRecords,
            min_distance: this.minimumDistance,
          },
        });
        if (Object.prototype.hasOwnProperty.call(response.data.data.Get, "Video_text_description")) {
          this.results = response.data.data.Get.Video_text_description;
        } else if (Object.prototype.hasOwnProperty.call(response.data.data.Get, "Video_text")) {
          this.results = response.data.data.Get.Video_text;
        } else {
          this.results = response.data.data.Get.Video_description;
        }
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
    // Method to generate the video link based on video ID, start time, and end time
    generateVideoLink(videoId, startTime, endTime) {
      const videoLink = `https://gallo.case.edu/cgi-bin/snippets/newsscape_mp4_snippet.cgi?file=${videoId}&start=${startTime}&end=${endTime}`;
      return videoLink;
    },
    // Method to download the results as a CSV file
    
    generateCSVRow(data) {
      const csvValues = Object.values(data);
      const formattedValues = csvValues.map((value) => {
        // Check if the value contains commas or double quotes, and escape them if necessary
        if (/[,"]/.test(value)) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value;
      });
      return formattedValues.join(",");
    },

    // Method to download the results as a CSV file
    downloadCSV() {
      const csvData = this.results.map((result) => {
        return {
          "Video ID": result.video_id,
          Text: result.text,
          "Start Time": result.starttime,
          "End Time": result.endtime,
          Metadata: result.metadata,
          Distance: result._additional.distance,
          "Video Link": this.generateVideoLink(result.video_id, result.starttime, result.endtime),
        };
      });

      const headers = Object.keys(csvData[0]);
      const csvRows = [headers.map((header) => `"${header}"`).join(",")];

      csvData.forEach((data) => {
        const row = this.generateCSVRow(data);
        csvRows.push(row);
      });

      const csvContent = csvRows.join("\r\n");
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      saveAs(blob, "search_results.csv");
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
  position: relative; /* Needed for positioning the tooltip */
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: border-color 0.3s ease; /* Add a smooth transition on border color change */
}

/* Style for tooltip */
.tooltip {
  position: absolute;
  top: -30px; /* Adjust the position of the tooltip above the input field */
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 5px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s, visibility 0.2s;
  pointer-events: none; /* Prevent the tooltip from affecting the input interaction */
}

.input-group:hover .tooltip {
  opacity: 1;
  visibility: visible;
}

/* Style for input fields when hovered */
input[type="text"]:hover,
input[type="number"]:hover {
  border-color: #007bff; /* Change the border color on hover */
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

.download-button {
  padding: 10px 20px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}

.download-button:hover {
  background-color: #218838;
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

.additional-info {
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
