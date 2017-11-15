<template>

</template>

<script>
import auth from './index'

export default {
	data() {
		return {
			credentials: {},
			errors: []
		}
	},
	methods: {
		login() {
			auth.login(this, this.credentials, {name: 'index'})
		}
	}
}

</script>
<style lang="scss">
</style>

