<template class="left">

  <div class="top">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-default/index.css">
    <link href="https://fonts.googleapis.com/css?family=Didact+Gothic" rel="stylesheet">

    <header class="main_header">
			<router-link class="ele logo-wrap" :to="'/'" >
				<a href="" class="main_logo">
					<img src="../assets/logo.png" >
				</a>
			</router-link>

      <router-link v-if="auth.isAuth" :to="'/'+auth.user.username" >
        <div v-if="auth.isAuth" class="user">
          <span class="user_name">
            {{auth.user.username}}
          </span>
          <img class="user_logo" :src="auth.user.avatar" alt="">
        </div>
      </router-link>

      <div v-on:click="switch_menu_opening()" class="open_user"></div>
      <div :class="{active : menu_opened }" class="user_menu">

				<router-link v-if="auth.isAuth" class="a_icn" :to="{name: 'userProfile', params: {user: auth.user.username}}">
					{{ $t("profile.profile") }}
				</router-link>

				<router-link v-if="auth.isAuth" class=" a_icn" :to="'/wallet'" >
					{{ $t("base.my_wallet") }}
				</router-link>


				<router-link :to="'/ico/'" class="a_icn" v-if="auth.isAuth">
				 <i class="fa fa-bitcoin"></i>
					ICO
				</router-link>

				<router-link :to="{name: 'login'}" class="a_icn" v-if="!auth.isAuth">
					Вход
				</router-link>

				<router-link :to="{name: 'signUp'}" class="a_icn" v-if="!auth.isAuth">
					Регистрация
				</router-link>

        <div class="a_icn lang_switcher" v-on:click="changeLocale()">
          <a href="">{{ auth.user.locale }}</a>
        </div>

        <a class="a_icn" href="">FAQ</a>

					<a  v-if="auth.isAuth" class="a_icn" @click="logout()" >
						{{ $t("base.logout") }}
					</a>


        </el-dropdown-item>

      </div>
    </header>
     </div>

</template>

<script>
import Vue from 'vue';
import auth from '../auth'
import {
    icon,
} from 'vue-fontawesome';
 export default {
   data() {
     return {
       auth: auth,
       menu_opened:false,
     }
   },
   methods: {
      switch_menu_opening(){
        this.menu_opened = !this.menu_opened
      },
     logout() {
       auth.logout(this)
     },
     changeLocale() {
      Vue.config.lang == 'en' ? Vue.config.lang = 'ru' : Vue.config.lang = 'en'
      this.auth.user.locale=Vue.config.lang
     },
   },
   components: {
    'vf-icon': icon,

   },
   created() {
        this.auth.user=auth.user
   },
 }
</script>

<style lang="scss">
.el-dropdown {
    color: #ffffff;
}
.lang_switcher{
  display: inline-block;
  font-weight: bold;
  padding: 0px 10px
}
#app{
    padding-top: 2%;
}

.ele{
  border-radius: 15px;
  display: inline-block;

  padding: 5px 10px;
  text-align: center;
  margin-bottom: 5px;
  cursor: pointer;
  font-family: 'Helvetica','Verdana','Arial'
}
.el-dropdown{
    cursor: pointer;
}
.top{
  position: fixed;
  top: 0;
  display: table;
  z-index: 12;
  width: 100%;
  color: #f6f7f7;

  background-color: #495565;
  border-bottom: #080808;
  padding: 8px 0px 5px 0px;

  .avatar{
    width: 25px;
    height: 25px;
    border-radius: 25px;
  }

  .login-box{
    display: inline-block;
    float: left;
    width: 25%;
    color: #fff;

  }
  .top-nav{
    display: inline-block;
    width: 75%;
    float: left;
    .ele{
      font-weight: normal;
    }
  }
}

.top .logo-wrap{
  padding: 1px 10px;
}
.top .ele b{

  vertical-align: middle;
}
.logo{
  width: 30px;
  height: auto;
  font-weight: normal;
  vertical-align: middle;
}

.el-dropdown {
	color: #fff;
}

.main_header{
	width: 100%;
	height: 62px;
	background-color: #485465;
	position: fixed;
	z-index: 100;
	top: 0;
	left: 0;
	display: flex;
	align-items: center;
}
.main_logo{
	display: block;
	width: 125px;
	height: 47px;
	margin-left: 55px;
}

.main_logo img{
	display: block;
}

.main_header .open_user{
	width: 92px;
	height: 100%;
	border-left: 1px solid #3b404c;
	position: absolute;
	right: 0;
	top: 0;
	cursor: pointer;
	background-image: url('../assets/arrow-down.svg');
	background-repeat: no-repeat;
	background-position: 25px center;
}

.main_header .user{
	right: 93px;
	top: 0;
	position: absolute;
	display: flex;
	align-items: center;
	height: 100%;
	padding: 0 17px 0 40px;

}
.main_header .user_name {
	opacity: 0.8;
	color: #fff;
	font-size: 16px;
	font-weight: 700;
}
.main_header .user_logo {
	margin-left: 11px;
	width: 40px;
	border-radius: 40px;
	height: 40px;
	object-fit: cover;
}

.main_header .user_menu{
	display: none;
	border-radius: 6px;
	background-color: #ffffff;
	box-shadow: 0 0 4px 0 rgba(139, 139, 139, 0.5);
	padding: 12px 17px;
	position: absolute;
	right: 17px;
	top: 62px;
	box-sizing: border-box;
}

.main_header .user_menu.active{
	display: block;
}

.main_header .user_menu:before{
	content: '';
	position: absolute;
	top: -8px;
	right: 35px;
	width: 0px;
	height: 0px;
	border-top: 18px solid #fff;
	border-left: 18px solid transparent;
	transform: rotateZ(-45deg);
	z-index: 100;
	box-shadow: 2px -2px 4px -1px rgba(139, 139, 139, 0.5);

}

.main_header .user_menu a{
	text-decoration: none;
	display: block;
	opacity: 0.87;
	color: #000;
	font-size: 16px;
	font-weight: 700;
	padding: 10px 0 10px 55px;
	position: relative;
}

.main_header .user_menu a.a_icn:before{
	width: 24px;
	height: 24px;
	position: absolute;
	display: block;
	content: '';
	left: 0;
	top: 8px;
	background: #d8d8d8;
}

</style>
