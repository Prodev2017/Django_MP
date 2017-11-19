<template>
  <div class="login-form">
		<link href="https://fonts.googleapis.com/css?family=PT+Sans:400,700" rel="stylesheet">

		<div class="two tab_headers">
			<router-link :to="{name: 'login'}" class="tab_header">Вход</router-link>
			<router-link :to="{name: 'signUp'}" class="tab_header">Регистрация</router-link>
		</div>

		<div class="tabs">
			<router-view></router-view>
		</div>
	</div>
</template>

<style>
.login-form {
    max-width: 393px;
    width: 100%;
    margin: 30px auto;
    border-radius: 6px;
    background-color: #ffffff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
}

.tab_headers{
	display: flex;
}

.tab_headers.two .tab_header{
	width: 50%;
}



.tab_headers .tab_header.active{
	background: #ffffff;
	color: #000;
	opacity: 1;
}

.tabs .tab{
	padding: 31px 26px 16px;
}

.tabs .tab.active{
	display: block;
}

.login-form .inpt{
	border-radius: 6px;
		border: solid 1px rgba(72, 84, 101, 0.2);
		box-sizing: border-box;
		height: 37px;
	display: block;
		padding: 0 10px 0 40px;
		width: 100%;
		margin-bottom: 12px;
		position: relative;
		color: #000;
		font-size: 16px;
		opacity: 0.87;
}
.tab_headers .tab_header{
	height: 65px;
	font-weight: 700;
	background-color: #edeef3;
	opacity: 0.74;
	line-height: 65px;
	font-size: 18px;
	letter-spacing: -0.3px;
	color: #929292;
	text-align: center;
	cursor: pointer;
}
.login-form .inpt:focus{
	 box-shadow: 0 0 2px 0 #6d9ee1;
	 outline: 0;
	 opacity: 1;
}

.inpt_w{
	position: relative;
}


.login-form .inpt + label:before{
	position: absolute;
	content: '';
	display: block;
	width: 40px;
	left: 0;
	top: 0;
	height: 100%;
	background-repeat: no-repeat;
	background-position: center center;
}

.login-form .i-user + label:before{
	background-image: url('/static/svg/icon-user.svg');
}

.login-form .i-pass + label:before{
	background-image: url('/static/svg/icon-pass.svg');

}

.submit-button{
	border-radius: 6px;
		background-color: #6d9ee1;
		border: none;
		line-height: 52px;
		width: 100%;
		text-align: center;
		display: block;
		color: #ffffff;
		opacity: 0.87;
		font-weight: 700;
		font-size: 18px;
		margin-top: 13px;
		margin-bottom: 12px;
}

.login-form .forgot{
	color: #545555;
	opacity: 0.87;
	width: 100%;
	font-size: 16px;
	display: block;
	cursor: pointer;
	padding: 15px 0;
	text-align: center;
	text-decoration: none;
}

.login-form .forgot:hover{
	opacity: 1;
}

.ivite{
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
