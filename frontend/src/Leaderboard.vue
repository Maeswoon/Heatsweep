<template>
<h1>Leaderboard</h1>
<div class="leaderboard">
    <table class="leaderboard-table">
        <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>ELO</th>
        </tr>
        <tr
            v-for="(player, index) in leaderboard"
            :key="index">
            <td>{{index + 1}}</td>
            <td>{{ player.username }}</td>
            <td>{{ player.elo }}</td>
    </tr>
    </table>
    
</div>
</template>
<script lang="ts">
    import { defineComponent } from 'vue';

    export default defineComponent({
    name: 'Leaderboard',
    props: {
        leaderboard: null
    },
    });
</script>

<style scoped>
h1 {
    font-size: 50px
}

.leaderboard-table th {
    font-size: 30px;
    font-weight: bold
}

.leaderboard-table td {
    padding: 10px
}
.leaderboard-table tr {
    font-size: 20px
}

.leaderboard-table td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

.leaderboard-table tr:nth-child(odd) {
    background-color: #dddddd;
}
</style>
