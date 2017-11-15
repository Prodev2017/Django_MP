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

<template>
	<form class="tab">
		<div class="inpt_w">
			<input type="text" placeholder="Username" v-model="credentials.username"class="inpt i-user"><label></label>
		</div>
		<div class="inpt_w">
			<input type="password" placeholder="Password" v-model="credentials.password" class="inpt i-pass"><label></label>
		</div>
		<div v-for="error in Object.keys(errors)">
			 <i class="el-icon-warning"></i> {{error}}: {{errors[error][0]}}
		</div>
		<div class="submit-button" @click="signUp">Зарегистрироваться</div>
		<a class="forgot" href="">Забыли пароль?</a>
	</form>
</template>



<style lang="scss" scoped>
</style>
