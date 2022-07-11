<template>
<div class="container" @click="clickHandle">
<div class="message">{{msg}}</div>
<!-- <i-button bind:click="handleClick" type="success" shape="circle" size="large">大尺寸</i-button> -->
<van-button type="default">默认按钮</van-button>
</div>
</template>

<script>
export default {
  data () {
    return {
      msg: 'Hello'
    }
  },

  methods: {
    clickHandle () {
      this.msg = 'Clicked!!!!!!'
    }
  }
}
</script>

<style scoped>
.message {
color: red;
padding: 10px;
text-align: center;
}
</style>
