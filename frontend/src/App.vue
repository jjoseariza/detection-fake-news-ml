<template>
  <div id="app">
    <h1>Fake news Detector</h1>
    <div v-if="result" class="container">
      <h3>The news is {{ result }}</h3>
      <div>Is this correct?</div>
      <div v-if="!feedback">
        <button class="btn btn-success" @click="onCorrect" :disabled="loading">
          Correct
        </button>
        <button
          class="btn btn-danger ml-5"
          @click="onWrong"
          :disabled="loading"
        >
          Wrong
        </button>
      </div>
      <div v-else>
        <button v-if="!loading" class="btn btn-primary" @click="onOther">
          Try other news
        </button>
      </div>
      <div v-if="loading" class="spinner-border text-primary" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
    <div v-else class="container">
      <div class="form-group">
        <label for="title">Title</label>
        <input
          type="title"
          class="form-control"
          id="title"
          v-model="title"
          placeholder="Enter the title of the news"
          :disabled="loading"
        />
      </div>
      <div class="form-group">
        <label for="text">Body</label>
        <textarea
          class="form-control"
          id="text"
          v-model="text"
          placeholder="Enter the body of the news"
          :disabled="loading"
        />
      </div>
      <button
        class="btn btn-primary"
        v-if="!loading"
        @click="onCheck"
        :disabled="!title || !text"
      >
        Check news
      </button>
      <div v-else class="spinner-border text-primary" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

// const endpoint = "https://tfm-api.azurewebsites.net";
const endpoint = "http://localhost:5000";

export default {
  name: "App",
  data() {
    return {
      title: "",
      text: "",
      result: null,
      loading: false,
      feedback: false,
    };
  },
  methods: {
    async onCheck() {
      if (!this.title || !this.text) return;
      this.loading = true;
      const { data } = await axios.post(`${endpoint}/predict`, {
        title: this.title,
        text: this.text,
      });
      this.result = data.result;
      this.loading = false;
    },
    onOther() {
      this.title = "";
      this.text = "";
      this.result = null;
      this.loading = false;
    },
    onCorrect() {
      this.feedback = true;
    },
    async onWrong() {
      this.loading = true;
      await axios.post(`${endpoint}/store-wrong`, {
        title: this.title,
        text: this.text,
        label: !this.result,
      });
      this.feedback = true;
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
h1 {
  margin-bottom: 20px;
}

.container {
  min-height: 300px;
}
.container div {
  margin: 10px 0;
}
textarea {
  min-height: 400px;
}
</style>
