<template>
<div class="profile">
	<div class="head_img" style="background-image: url(); background-color: #6d9ee1;">
		<i class="back"></i>
	</div>
	<div class="user">
		<div class="round_av edit_av">
			<i class="ic delete"></i>
			<i class="ic edit" @click="$refs.avatarInput.click()">
				<input ref="avatarInput" @change="setAvatar" hidden type="file">
			</i>
	
			<!-- аватар в img -->
			<img :src="auth.user.avatar">
		</div>
		<div class="name verified">@{{ auth.user.username }}</div>
	</div>
	
	<div class="inpt_w">
		<label for="city">Показывать город по умолчанию</label>
		<input type="text" name="city" id="city">
	</div>
	<div class="inpt_w">
		<label>Username</label>
		<input v-model="auth.user.username"  type="text">
	</div>
	<div class="inpt_w">
		<label>Email</label>
		<input type="email" v-model="auth.user.email">
	</div>
	<div class="inpt_w">
		<label for="c_pass">Изменить пароль</label>
		<input type="password" v-model="auth.user.password" placeholder="Новый пароль">
	</div>
	<div class="inpt_w">
		<label for="keys">Ключи от аккаунта</label>
		<input type="text" v-model="auth.user.posting_key">
	</div>
	<button class="submit" @click="update()">Обновить</button>

	<div class="p_h">Привязать профили социальных сетей</div>
	<div class="socials">
		<a href="" class="soc_icon fb"></a>
		<a href="" class="soc_icon in"></a>
		
		<div class="more">
			<div class="soc_square">
				<i class="sq_soc tw"></i>	
				<i class="sq_soc fb"></i>	
				<i class="sq_soc tg"></i>	
				<i class="sq_soc gp"></i>	
			</div>
			<div class="connect_m">Connect <br> More Accounts</div>
			<div class="add">
				<a href="" class="soc_icon tg"></a>
				<a href="" class="soc_icon gp"></a>
			</div>
		</div>
	</div>
	<div class="ivite">Моя реферальная ссылка: <span class="blue">jbrgfnJG7vee</span></div>
</div>
</template>

<script>
import Vue from 'vue'

import auth from '../auth'
import {User} from '../services/services'


export default {
    name: 'Profile',
    data () {
        return {
            error: false,
            auth: auth,
        }
    },

    methods:{
      update() {
				User.update({id: this.auth.user.id}, this.auth.user).then(res => {
					this.auth.user = res.body
								this.$message({
								type: 'info',
										message: `Профиль обновлен`
								})
				}, res => {
					this.error = res.data.error;
					this.$message({
					type: 'error',
						message: 'неправильный ключ'
					});
				})
      },

      setAvatar(e) {
				e.preventDefault()

        let formData = new FormData()
        formData.append('file', this.$refs.avatarInput.files[0])

        User.setAvatar({id: this.auth.user.id}, formData).then(res => {
          auth.user.avatar = res.body
            this.$message({ type: 'info', message: 'Аватар обновлен' })
        }, res => {
            this.error = res.data.error;
            this.$message({ type: 'error', message: 'Что то пошло не так'})
        })
      },
    },
}
</script>

<style>
.profile{
	margin: 20px auto;

	max-width: 658px;
	width: 100%;
	border-radius: 6px;
	background-color: #ffffff;
	box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
	border: solid 1px rgba(72, 84, 101, 0.2);
	box-sizing: border-box;
}

.profile .head_img{
	background-repeat: no-repeat;
	background-size: cover;
	background-position: center;
	background-color: #ddd;
	width: 100%;
	height: 160px;
	position: relative;
	border-top-left-radius: 6px;
	border-top-right-radius: 6px;
}

.profile .user {
	position: relative;
	z-index: 5;			
	margin: -60px auto 55px auto;
	text-align: center;
}

.profile .round_av {
	width: 120px;
	height: 120px;
	border-radius: 50%;
	margin: 0 auto 20px;
	display: block;
	background: url(../assets/profile/icon-profile.svg) #fff no-repeat;
	background-size: cover;
	position: relative;
}

.profile .edit_av {
	background: url(../assets/icon-close.svg) #485466 no-repeat center center;
	cursor: pointer;
}

.profile .round_av img {
	width: 100%;
}

.profile img {
	display: block;
}

.profile .ic {
	width: 60px;
	height: 60px;
	background-color: #ffffff;
	box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
	position: absolute;
	background-position: center center;
	background-repeat: no-repeat;
	top: 30px;
	border-radius: 50%;
}

.profile .ic.delete {
	background-image: url(../assets/profile/icon-trash.svg);
	left: -80px;
}

.profile .ic.edit {
	background-image: url(../assets/icon-edit.svg);
	right: -80px;
}

.profile .user .name {
	font-size: 26px;
 	font-weight: 700;
	color: #485465;
	text-align: center;
	position: relative;
	display: inline-block;
}

.profile .user .name.verified:before {
	position: absolute;
	content: '';
	width: 21px;
	height: 21px;
	background: url(../assets/icon-blue-check.svg) no-repeat;
	top: -9px;
	right: -24px;
}

.profile .submit {
	border-radius: 6px;
		background-color: #6d9ee1;
		border: 0;
		margin: 0 auto;
		line-height: 37px;
		opacity: 0.87;
		font-size: 16px;
		font-weight: 700;
		color: #fff;
		width: 290px;
		display: block;
		margin-bottom: 40px;
		margin-top: 36px;
}
.profile [type="submit"]:hover{
	opacity: 1;
}

.profile label{
	font-size: 18px;
	font-weight: 700;
	letter-spacing: -0.6px;
	color: #333;
	display: block;
	margin-bottom: 12px;
}

.profile .inpt_w{
	position: relative;
	margin: 0 30px 0 50px;
}

.profile input[type="text"],
.profile input[type="email"],
.profile input[type="password"]{
	height: 38px;
	border-radius: 4px;
	border: solid 1px #efefef;
	box-sizing: border-box;
	display: block;
	margin-bottom: 22px;
	padding: 0 18px;
	outline: 0;
	font-size: 16px;
	opacity: 0.87;
	color: #000;
	width: 100%;
}

.profile input[type="text"]:focus,
.profile input[type="email"]:focus,
.profile input[type="password"]:focus{ 
	box-shadow: 0 0 2px 0 #6d9ee1;
		border: solid 1px rgba(0, 105, 255, 0.2);
		opacity: 1;
}

.profile .back{
	width: 42px;
	height: 42px;
	display: block;
	position: absolute;
	z-index: 5;
	background: url(../assets/icon-arrow-left.svg) no-repeat center center;
	top: 12px;
	left: 12px;
	cursor: pointer;
}

.profile .p_h{
	font-size: 18px;
	font-weight: 700;
	letter-spacing: -0.6px;
	color: #000;
	margin: 0 0 30px 50px;
}

.profile .socials{
	width: 100%;
	height: 50px;
	margin-bottom: 60px;
	padding-left: 50px;
	display: flex;
}

.profile .socials .soc_icon{
	display: block;
	width: 50px;
	height: 50px;
	border-radius: 50%;
	margin-right: 15px;
	background-position: center;
	background-repeat: no-repeat;
}

.profile .socials .soc_icon:hover{
	background-color: #E04F5F !important;
	background-image: url(../assets/icon-close.svg) !important;
}

.profile .socials .soc_icon.fb{
	background-color: #3b5998;
	background-image: url(../assets/icon-fb.svg);
}

.profile .socials .soc_icon.in{
	background-color: #55acee;
	background-image: url(../assets/icon-tw.svg);

}

.profile .socials .soc_icon.tg{
	background-color: #62a5d7;
	background-image: url(../assets/icon-tg.svg);
}

.profile .socials .soc_icon.gp{
	background-color: #dd4b39;
	background-image: url(../assets/icon-gp.svg);
}

.profile .socials .more{
	border-radius: 3px;
	border: solid 1px #ced7df;
	height: 50px;
	box-sizing: border-box;
	padding: 6px 16px 6px 6px;
	display: flex;
	align-items: center;
	cursor: pointer;
}

.profile .socials .more .soc_icon{
	width: 36px;
	height: 36px;
	margin-right: 12px;
	background-size: 24px;
}

.profile .socials .more .soc_icon:hover{
	background-image: url(../assets/icon-plus.svg) !important;
	background-color: #4fe0a7 !important;
}

.profile .socials .connect_m{
	font-size: 11px;
		color: #59626a;
		
}

.profile .more .add{
	display: none;
}

.profile .more.active{
	padding-right: 4px;
}

.profile .more.active .add{
	display: flex;
}

.profile .more.active .connect_m{
	padding-right: 25px;
		margin-right: 17px;
		border-right: solid 1px #ced7df;
}

.profile .soc_square{
	display: flex;
	flex-wrap: wrap;
	width: 36px;
	height: 36px;
	margin-right: 5px;
}

.profile .soc_square .sq_soc{
	background-repeat: no-repeat;
	background-position: center;
	width: 18px;
	height: 18px;
	opacity: .8;	
}

.profile .soc_square .tw {
	background-image: url(../assets/icon-tw.svg);
	background-color: #64b2dd;
	background-size: 76%;
	border-top-left-radius: 2px;
}

.profile .soc_square .fb {
	background-image: url(../assets/icon-fb.svg);
	background-color: #3b5998;
	background-size: 40%;
	border-top-right-radius: 2px;
}

.profile .soc_square .tg {
	background-image: url(../assets/icon-tg.svg);
	background-color: #62a5d7;
	background-size: 78%;
	border-bottom-left-radius: 2px;
}

.profile .soc_square .gp {
	background-image: url(../assets/icon-gp.svg);
	background-color: #dd4b39;
	background-size: 81%;
	border-bottom-right-radius: 2px;
}

.ivite {
    line-height: 60px;
    letter-spacing: -0.7px;
    font-weight: 700;
    font-size: 20px;
    padding: 0 41px;
    background-color: #fbfbfb;
    display: inline-block;
    margin: 0 0 86px 50px;
}

</style>
