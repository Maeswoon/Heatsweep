<template>
    <h1>Lobby</h1>
    <div class="lobby">
        <table class="lobby-table">
            <tr>
                <th>Game</th>
                <th>Player</th>
                <th>Join Game</th>
            </tr>
            <tr
                v-for="(game, index) in games"
                :key="index">
                <td><div class="item-container">{{ game.id }}</div></td>
                <td><div class="item-container">{{ game.player_a.username }}</div></td>
                <td><div class="item-container"><button class="join-button" @click="handler(game.id)">Join</button></div></td>
            </tr>
        </table>
    </div>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';

    export default defineComponent({
    name: 'Lobby',
    props: {
        games: null,
        handler: null
    },
    });
</script>

<style scoped>
h1 {
    font-size: 50px;
    text-align: center;
}

.lobby-table th {
    font-size: 30px;
    font-weight: bold
}

.lobby-table td {
    padding: 10px
}
.lobby-table tr {
    font-size: 20px
}

.lobby-table td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

.lobby-table tr:nth-child(odd) {
    background-color: #dddddd;
}

.item-container {
    max-width: fit-content;
    margin: 0 auto;
}

.join-button {
    font-size: 20px;
    padding: 10px;
    background-color: #00cf11;
    border-radius: 8px;
    border-width: 0;
    cursor: pointer;
}
</style>
