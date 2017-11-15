import {User} from '../services/services'

const JWT_AUTH_URL = '/api-auth/'

export default {
  isAuth: false,
  user: {
		username: ' '
	},

  login(context, creds, redirect) {
    context.$http.post(JWT_AUTH_URL, creds).then(res => {
      localStorage.setItem('jwt', res.body.token)

      this.isAuth = true
			this.user = res.body.user

      if (redirect) { context.$router.push(redirect) }

    }, res => {
      console.log('LOGIN ERR', res.body)
      context.errors = res.body })
  },

  signUp(context, creds, redirect) {
    User.signUp(creds).then(res => {

      localStorage.setItem('jwt', res.body.token)
      this.isAuth = true
			this.user = res.body.user

      if (redirect) { context.$router.push(redirect) }

    }, res => { context.errors = res.body


      console.log('res ERR',res.body)
     })
  },

  logout() {
    localStorage.removeItem('jwt')

    this.isAuth = false
		this.user = {}
  },

  checkAuth() {
		this.isAuth = !!localStorage.getItem('jwt') ? true : false

		// Запросим юзера при старте приложения
		if (this.isAuth) { User.current().then(res => this.user = res.body) }
	},

  getAuthToken() {
			let token = localStorage.getItem('jwt')
      return !!token ? 'JWT ' + token : null
  }
}
