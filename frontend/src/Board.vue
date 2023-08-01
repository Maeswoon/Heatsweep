<template>
  <div class="board">
    <div v-if="game && game.player_a" class="player-info-container">
      <h2>{{ game.player_a.username }} <span style="color: #2eb52e">◼</span></h2>
      <h3>Player A</h3>
      <h3>ELO: {{ game.player_a.elo }}</h3>
    </div>
    <div class="grid">
      <button :class="['board-tile', tile.status == 'a' ? 'a-tile' : (tile.status == 'b' ? 'b-tile' : ''), 
    tile.x == game.a_x && tile.y == game.a_y ? 'a-start' : (tile.x == game.b_x && tile.y == game.b_y ? 'b-start' : '')]"
          :style="{'background-color': tile.heat_value}"
          v-for="(tile, index) in tiles"
          :key="index"
          @click="handler(index)"
      >
      </button>
    </div>
    <div v-if="game && game.player_b" class="player-info-container">
      <h2>{{ game.player_b.username }} <span style="color: #5c5cff">◼</span></h2>
      <h3>Player B</h3>
      <h3>ELO: {{ game.player_b.elo }}</h3>
    </div>
    <h2 v-if="game && game.player_a && game.player_b && game.current_turn">It is {{ game.player_a.username == game.current_turn.username ? game.player_a.username : game.player_b.username }}'s turn</h2>
    <h1 v-if="winner">{{ winner }}</h1>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Board',
  props: {
    game: null,
    tiles: null,
    handler: null
  },
  data() {

  },
  computed: {
    winner() {
      if (!this.game || !this.game.winner) return;
      return `Player ${this.game.winner.username} wins!`;
    },
  },
  methods: {
    computeColor(val: number) {
      var r = 255
      var g = 255 * val
      var b = g
      return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}`
    }
  }
});
</script>

<style scoped>
:root {
  --a: #5cff5c;
  --b: #5c5cff;
}

h1 {
    font-size: 30px;
    text-align: center;
}
.grid {
  display: grid;
  grid-template-columns: repeat(7, 3rem);
  grid-template-rows: repeat(7, 3rem);
  grid-gap: 0.3rem;
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  /*background-image: linear-gradient(to top right, rgb(115, 115, 226), rgb(177, 174, 204));*/
}
button {
  font-size: 1rem;
  font-family: monospace;
}
.board-tile {
  /** border-radius: 4px;
  border-style: solid;
  border-width: 4px; **/
  cursor: pointer; 
  border-style: solid;
  border-width: 1px;
  border-radius: 2px;
}
.a-tile {
  border-style: solid;
  border-width: 4px;
  border-color: #2eb52e;
}
.b-tile {
  border-style: solid;
  border-width: 4px;
  border-color: #5c5cff;
}
.a-start {
  background-color: #2eb52e !important;
}
.b-start {
  background-color: #5c5cff !important;
}
</style>
