<template>
	<form class="tab">
		<div class="inpt_w">
			<input type="text" placeholder="Username" v-model="credentials.username" class="inpt i-user"><label></label>
		</div>
		<div class="inpt_w">
			<input type="password" placeholder="Password" v-model="credentials.password" class="inpt i-pass"><label></label>
		</div>
		<div v-for="error in Object.keys(errors)">
			 <i class="el-icon-warning"></i> {{error}}: {{errors[error][0]}}
		</div>
		<div class="submit-button" @click="login">Войти</div>
		<a class="forgot" href="">Забыли пароль?</a>
	</form>
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

