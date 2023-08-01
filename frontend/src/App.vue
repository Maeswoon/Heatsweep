<template>
  <div class="app-header">
    <div class="header-right">
      <input v-if="!isLoggedIn" type="text" class="login-input" v-model="username_input" placeholder="Username">
      <button v-if="!isLoggedIn" class="header-button" @click="login()">Login</button>
      <div v-else class="header-container">
        <h2>
          Welcome Back, {{ username }}
        </h2>
        <button class="create_button" @click="createGame()">New Game</button>
      </div>
      <button @click="toggleLeaderboard" class="header-button">
        {{ leaderboardShown ? "Hide Leaderboard" : "Show Leaderboard" }}
      </button>
    </div>
  </div>
  <div class="app-content">
    <Lobby v-if="availableGames && gameId == -1 && !leaderboardShown" :games="availableGames" :handler="joinHandler"/>
    <Board v-if="state && !leaderboardShown && gameId != -1" :game="state.game" :tiles="state.tiles" :handler="flipHandler"/>
    <Leaderboard v-if="leaderboardShown" :leaderboard="leaderboard"></Leaderboard>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import Board from './Board.vue'
import Leaderboard from './Leaderboard.vue'
import Lobby from './Lobby.vue'

const BACKEND = "http://localhost:8000"

export default {
  name: 'App',

  components: {
    Board,
    Leaderboard,
    Lobby
  },
  data() {
    return {
      state: {
        game: null,
        tiles: null
      },
      poller: 0,
      gameId: -1,
      polling: false,
      leaderboardShown: false,
      leaderboard: null,
      availableGames: null,
      username_input: "",
      username: ""
    }
  },
  methods: {
    joinHandler: function(id: number) {
      if (!this.isLoggedIn) {
        console.error("Can't join, not logged in")
      }
      axios.post(BACKEND + `/lobby/join/${id}/${this.username}/`)
      .then(response => {
        this.gameId = response.data.id
        this.poll()
        this.polling = true
      })
      .catch(error => {
        console.error(error);
      });
    },
    flipHandler: function(index:number) {
      if (this.gameId != -1 && this.isLoggedIn) {
        axios.post(BACKEND + `/game/flip/${this.gameId}/${this.username}/${index}/`)
        .then(_ => this.poll)
        .catch(error => {
          console.error(error);
        });
      } else {
        console.error("Muse be logged in and joined to flip")
      }
    },
    poll: function() {
      if (this.polling) {
        axios.get(BACKEND + `/game/${this.gameId}/`)
        .then(response => {
          this.state = response.data
        })
        .catch(error => {
          console.error(error);
        });
      }
      
    },
    stopPolling: function() {
      this.polling = false
    },
    toggleLeaderboard: function() {
      this.leaderboardShown = !this.leaderboardShown
    },
    refreshLobby: function() {
      axios.get(BACKEND + '/lobby')
      .then(response => {
        this.availableGames = response.data
      })
      .catch(error => {
        console.error(error);
      });
    },
    login: function() {
      if (this.username_input != "") {
        axios.post(BACKEND + `/player/${this.username_input}/`)
        .then(response => {
          this.username = this.username_input
        })
        .catch(error => {
          console.error(error);
        });
      } 
    },
    createGame: function() {
      if (this.username != "") {
        axios.post(BACKEND + `/game/create/${this.username}/`)
        .then(response => {
          this.state = response.data
          this.gameId = response.data.game.id
          this.polling = true
        })
        .catch(error => {
          console.error(error);
        });
      }
    }
  },
  computed: {
    isLoggedIn() {
      return this.username != ""
    }
  },
  mounted() {
    this.refreshLobby()
    this.poller = setInterval(this.poll, 500)
    axios.get(BACKEND + '/leaderboard/')
    .then(response => {
      this.leaderboard = response.data
    })
    .catch(error => {
      console.error(error);
    });
  },
  unmounted() {
    clearInterval(this.poller)
  }
}
</script>

<style>
.app-header {
  width: 100%;
  font-size: 20px;
}
.app-header button {
  font-size: 20px;
  background-color: #4793ff;
  border-radius: 8px;
  border-width: 0;
  cursor: pointer;
  margin: 10px
}
.app-content {
  max-width: fit-content;
  margin: 10px auto
}
.header-left {
  margin-right: auto;
  margin-left: 0;
  max-width: fit-content
}
.header-container, .header-container h2 {
  max-width: fit-content;
  display: inline-block;
  margin: 0
}
.header-container h2 {
  margin: 10px
}
.header-right {
  margin-left: auto;
  margin-right: 0;
  max-width: fit-content
}
.header-right button {
  padding: 10px;
}
.login-input {
  padding: 10px;
  font-size: 20px;
  border-radius: 8px;
  border-style:solid;
}
</style>

