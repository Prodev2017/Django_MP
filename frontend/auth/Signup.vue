<template>

</template>

<script>
import auth from '../auth'

export default {
	data() {
		return {
			credentials: {},
			errors: []
		}
	},
  methods: {
		signUp() {
			auth.signUp(this, this.credentials, {name: 'index'})
		}
  }
}
</script>

<style lang="scss" scoped>
</style>
