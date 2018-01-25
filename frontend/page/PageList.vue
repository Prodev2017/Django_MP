<style src="vue2-animate/dist/vue2-animate.min.css"></style>
<template>
  <div>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css">

    <gmap-map
      :center="this.center"
      :zoom="this.my_zoom_size"

      ref="mmm"
      :clickable="true"
      :draggable="false"
      max-zoom="5"
      min-zoom="4"
      >

       <gmap-info-window
       :position="user_marker.position"
       :opened="true"
       :content="auth.user.username"></gmap-info-window>

			<google-marker
				v-for="m in markers"
				:key="m.id"
				:position="m.position"
				:clickable="true"
				:draggable="false"
				@click="scrollTo(m.page_id)">
			</google-marker>

      <gmap-info-window
				v-for="m in markers"
				:options="infoOptions"
				:position="m.position"
				:opened="true"
				:content="'<b>'+m.author+'</b><br>' + ' ' + m.pay_out + ' ₽'  "
				:key="m"
				@closeclick="infoWinOpen=false">
			</gmap-info-window>

    </gmap-map>
    <div class="wrapper">
      <div class="page-list">
        <div v-if="loading" class="loader">
          <i class="el-icon-loading"></i>
        </div>
        <div>
        <div v-if="this.author" class="profile">
          <img :src="author.avatar" alt="" class="author_avatar">
          <div class="username">
            @{{author.username}}
          </div>
          <div v-if="author.username == auth.user.username " class="self_blog_view_buttons">
            <div class="half">
              <i class="fa fa-bitcoin"></i> Кошелек
            </div>
            <div class="half">
              <router-link :to="'/profile'">
                  <div v-if="auth.isAuth"  >
                      <div >
                       <i class="fa fa-gear"></i>  Настройки
                      </div>
                  </div>
              </router-link>
            </div>
          </div>
        </div>
          <div v-if="pages.length==0">...</div>
          <router-link :to="'/add/'" v-if="auth.isAuth">
           <i class="fa fa-plus"></i>
          {{ $t("base.add") }}
          </router-link>

          <div class="article animated" v-for="page in pages" :id="'page_id_'+ page.id" v-bind:key="page">
            <div>
              <img v-if="page.miniature" class="post-image" :src="page.miniature" alt="" onerror="this.style.display='none'">
            </div>
            <div class="post-preview">
              <div class="post-info">
                <div class="avatar">
                  <img v-if="page.author_avatar" :src="page.author_avatar" alt="" >
                </div>
                <div class="head">
                  <router-link :to=" '/'+ page.author"> {{page.author}}</router-link>  <i class="fa fa-map-marker" v-if="page.position_text"> {{page.position_text}}</i>
                  <br/>
                  <i class="fa fa-date" ></i>{{page.created_at || page.updated_at | formatDate}}
                  <br/>
                </div>
              </div>
              <div class="full">
                <router-link :to="{name: 'page', params: {user: page.author, permlink: page.permlink} }">
                  <h4>{{page.title}}</h4>
                  <span>
                    {{page.body.replace(/<\/?[^>]+(>|$)/g, "")}}
                  </span>
                </router-link>
              </div>
            </div>
              <div class="bottom">
                <div class="comments one-fourth">
                 &nbsp;<!-- <div v-if="page.last_comments.length > 0"><i class="fa fa-comment-o"></i>&nbsp;{{page.comments.length}}&nbsp;{{page.comments.length | sayCommentsLength}}</div> -->
                </div>
                <div class="comments one-fourth">
                  <a v-on:click="share('vkontakte',getPageUrl(page), page.title,'IMG_PATH', 'page.body Mapala.net Everyone can travel'  )"> <i class="fa fa-share"></i> Рассказать</a>

                </div>
                <div class="half">
                  <div class="button" v-on:click="vote(page)">
                    <i class="fa fa-dot-circle-o"></i>
                    <span>Поддержать</span> | <i class="fa fa-rub"></i> {{page.total_pending_payout_value}}
                  </div>
                  Поддержало {{page.voters.length}}
                </div>
              </div>
              <div class="comments-wrapper">
                <comments
                  class="comments"
                  v-for="comment in page.last_comments"
                  :key="comment.id"
                  :model="comment">
                </comments>
                <div v-if="page.last_comments.length > 0" v-on:click="moreComments(page)" class="load-more">Показать предыдущие комметарии</div>

              </div>
          </div>
        </div>

      </div>
      <Right></Right>
    </div>

    <mugen-scroll tag="mu" :handler="fetchPage" :should-handle="!loading">

      &nbsp;
    </mugen-scroll>
    </div>
</template>
<script>
import Comments from './Comments.vue'
import Vue from 'vue'
import auth from '../auth'
import Top from '../base/Top.vue'
import Right from '../base/Right.vue'
import InputTag from 'vue-input-tag'
import finance from '../services/finance'
import MugenScroll from 'vue-mugen-scroll'
import {Page, Comment} from '../services/services'
import {User} from '../services/services'
var VueScrollTo = require('vue-scrollto');
Vue.use(VueScrollTo)



Vue.filter('sayCommentsLength', function(value) {

    if (value==0){
      return 'Комментарев'
    }
    else if (value==1){
      return 'Комментарий'
    }
    else if (value==2){
      return 'Комментария'
    }
    else if (value==5){
      return 'Комментариев'
    }
    return "XXX  ---"
})


export default {
  name: 'PageList',
  data () {
    return {
      center: {
        lat: 10.0,
        lng: 10.20
      },
      position: {},
      author:null,
      blog_view:false,
      self_blog_view:false,

      my_zoom_size:5,
      markers:null,
      bounds:null,
      infoOptions: {
        pixelOffset: {
          width: 0,
          height: -35
        }
      },
      markers_loaded:false,
      user_marker:{
        lat: 10.0,
        lng: 0.0
      },


      auth: auth,
     // markers:[],
      // currency_sbd:finance.currency.sbd,
      pages: [],
      nex_page: 1,
      currency_sbd:null,
      loading: true,
      imgObj: {
        src: '/static/dist/logo.png',
        error: '/static/dist/logo.png',
        loading: '/static/dist/logo.png'
      },
      state4:''
    }
  },
  components: {
    'Top': Top,
    'Right': Right,
    'input-tag': InputTag,
    'mugen-scroll': MugenScroll,
    'VueScrollTo':VueScrollTo,
    'comments':Comments,
  },

  methods: {

    share(network_name, purl, ptitle, pimg, text){
      if (network_name=="vkontakte"){
        var vkontakte=function(purl, ptitle, pimg, text) {
          var url  = 'http://vkontakte.ru/share.php?';
          url += 'url='          + encodeURIComponent(purl);
          url += '&title='       + encodeURIComponent(ptitle);
          url += '&description=' + encodeURIComponent(text);
          url += '&image='       + encodeURIComponent(pimg);
          url += '&noparse=true';
          window.open(url,'','toolbar=0,status=0,width=626,height=436');
        }
        vkontakte(purl, ptitle, pimg, text)
      }
    },


    navigate:function(voter){
      this.$router.push('/'+voter)
    },
    makeMarkers(){

      var prepared_markers=[]
      var pos_pages=this.pages.filter(function(e){return e.position && typeof(e.position.latitude)!="undefined" && e.position && typeof(e.position.longitude)!="undefined"  })
      if (pos_pages && pos_pages.length>0){
        for (var mar in pos_pages){
          try{
            var m={
              'page_id': this.pages[mar].id,
              'pay_out':this.pages[mar].total_pending_payout_value,
              'position':{
                'lat':parseFloat(this.pages[mar].position.latitude),
                'lng':parseFloat(this.pages[mar].position.longitude),

              },
              'radius':1000,
              'author':this.pages[mar].author
            }
            if (typeof(m)!="undefined"){
              prepared_markers.push(m)
            }
            else{
              //console.log('undef')
            }

          }
          catch(err){
            console.log('eee',err)
          }

          //console.log('putting',this.pages[mar].position.latitude, this.pages[mar].position.longitude)
        }
        //this.markers=prepared_markers
        this.$set(this,'markers', prepared_markers )
        //alert(prepared_markers[0])

      }
    },

    fetchPage () {
			this.loading = true

			let params = {}
			params.papage = this.nex_page
			if (!this.nex_page) { return }
			// Если на траниче пользователя
			let author = this.$route.params.author
			if (author) {
        params.author__username = author
        this.blog_view=true
        //console.log(this.$route.params.author, auth.user.username)
        if(this.$route.params.author==auth.user.username){
          this.self_blog_view=true;
        }
        else{
          this.self_blog_view=false;
        }
        var result=User.get({username:author}).then(res => {
           //console.log(username,'-->', res.body[0].avatar)
           var profile=res.body[0]
           //console.log('------> got:',ava)
           this.author=profile
        })

      }
      else{
        this.blog_view=false
      }
      if (!this.nex_page >= this.page){

      }
      if(this.nex_page==null){
        return null
        this.loading=false
      }
			Page.get(params).then(res => {
          this.pages = this.pages.concat(res.body.results)
          this.my_zoom_size=5
					// TODO Как должно работать? Пофиксить
          this.makeMarkers()
          if (this.markers && this.markers.length > 0){
            this.center={lat:this.markers[0].position.lat,lng:this.markers[0].position.lng}

          }
          this.my_zoom_size=3;

          //this.fitBounds()
					this.loading = false

					this.nex_page = res.body.next
			})
      this.loading=false
    },
    getPageUrl(page){
      return('http://'+window.location.hostname+'/'+page.author+'/'+page.permlink)
    },
    getFirstImage(body){
      try{
        var m,
            urls = [],
            //str = '<img src="http://site.org/one.jpg />\n <img src="http://site.org/two.jpg />',
            rex = /<img[^>]+src="?([^"\s]+)"?\s*\/>/g;
            //res='/\b(https?:\/\/\S*?\.(?:png|jpe?g|gif)(?:\?(?:(?:(?:[\w_-]+=[\w_-]+)(?:&[\w_-]+=[\w_-]+)*)|(?:[\w_-]+)))?)\b/'
        while ( m = rex.exec( body ) ) {
            urls.push( m[1] );
        }
        // console.log('URL_________>', urls );
          if (urls.length>0){
            return urls[0]
          }
          //var res = body.match(reg)
          //console.log('res',res)
      }
      catch(err){

      }
      return null
    },
    moreComments(page){
      //console.log('loadCOMMENTS')
      Comment.get({'page':page}).then(res => {
        //console.log('wohoo',res)
        page.last_comments = []
        page.last_comments = res.body
      })

    },
    getAvatar(page){
    var username= page.author
      var result=User.get({username:username}).then(res => {
         //console.log(username,'-->', res.body[0].avatar)
         var ava=res.body[0].avatar
         page.author_ava=ava
         console.log('ava',ava,page)
         page.avatar=ava
         return ava
      })

    },

    vote (page) {
      let voter = page.voters.find(id => id == auth.user.id)

      if (auth.isAuth) {
        if(!voter) {
          // upvote
          page.voters.push(this.auth.user.id)
        } else {
          page.voters = page.voters.filter(id => id != auth.user.id)
        }

        Page.update({permlink: page.permlink}, page).then(res => {
          this.$message({type: 'success', message: 'голос принят'})
          }, res => {
            this.$message({type: 'error', message: 'like error'})
          })
        }
      else {
        this.$message({
            type: 'warning',
            message: 'для того чтобы голосовать, нужно сначала авторизоваться'
        })
      }
    },


    scrollTo(page_id) {
      //Выполняет скролл к странице и мигает анимацией
      var options = {
          // container: 'app',
          // easing: VueScrollTo.easing['ease-in'],
          offset: -60,
          onDone: function() {
            // scrolling is done
          },
          onCancel: function() {
            // scrolling has been interrupted
          }
      }
      VueScrollTo.scrollTo('#page_id_'+page_id, 500, options)
      var elem=document.querySelector('#page_id_'+page_id)
      elem.classList.remove('flash')
      setTimeout(()=>elem.classList.add('flash'),100)
      // elem.classList.toggle('flash')
      //animated flash
    },
    /*MAP*/
    fitBounds() {
      //return 0
      if (this.bounds==null){
        try{
          this.bounds=new google.maps.LatLngBounds()
        }
        catch(err){

        }

      }
      //this.my_zoom_size=9
      console.log('fit bounds call')
      if (typeof(markers)!="undefined" && this.markers.length>0){
        var m=null
        if (typeof(markers)!="undefined" && !markers.position || typeof(markers)!="undefined" && !markeres.position.lat){
          return
        }
        for (m in this.markers){
          this.bounds.extend({
            lat: this.markers[m].position.lat,
            lng: this.markers[m].position.lng
          })
          console.log('bounds EXTENDED ',this.markers[m].position.lat ,this.markers[m].position.lng)
        }
        //Теперь создадим точку чтобы совсем близко не зумило
        //var extendPoint1 = new google.maps.LatLng(b.getNorthEast().lat() + 0.01, b.getNorthEast().lng() + 0.01);
        //var extendPoint2 = new google.maps.LatLng(b.getNorthEast().lat() - 0.01, b.getNorthEast().lng() - 0.01);
        //b.extend(extendPoint1);
        //b.extend(extendPoint2);


        this.$refs.mmm.fitBounds(this.bounds);

        //this.$refs.mmm.panToBounds(this.bounds);
        console.log('ZOOM CHANG??',this.my_zoom_size)
      }

    },

    //SEARCHBOX
    loadAll() {
      return [
        { "value": "Задания", "link": "https://github.com/vuejs/vue" },
        { "value": "Впечатления", "link": "https://github.com/ElemeFE/element" },
        { "value": "Где я?", "link": "https://github.com/ElemeFE/cooking" },
        { "value": "Развлечения", "link": "https://github.com/ElemeFE/mint-ui" },
        { "value": "События", "link": "https://github.com/vuejs/vuex" },
       ];
    },
    querySearchAsync(queryString, cb) {
      var links = this.links;
      var results = queryString ? links.filter(this.createFilter(queryString)) : links;

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 3000 * Math.random());
    },
    createFilter(queryString) {
      return (link) => {
        return (link.value.indexOf(queryString.toLowerCase()) === 0);
      };
    },
    handleSelect(item) {
      console.log(item);
    }
  },
  beforeRouteUpdate (to, from, next) {
     this.page_num=1
     next()
  },

  watch: {
		'$route'() {
      this.author=null;
			this.nex_page = 1
			this.pages = []
			this.fetchPage()
		},

  },
  computed:{

  },
  created: function () {
    // Get the coordinates of the current position.
    let position={}
    navigator.geolocation.getCurrentPosition(function(position) {

      // console.log('position.coords',position.coords)
      this.position={'lat':position.coords.latitude,'lng':position.coords.longitude}
      // position={'label':'YOU','position':{'lat':position.coords.latitude,'lng':position.coords.longitude} }
      position = {
        position:{
          'lat':position.coords.latitude,
          'lng':position.coords.longitude
        },
        statusText: "USER",
        draggable: true,
      }
      //this.markers=[]
      //this.user_marker=position

    // this.center=this.position

     auth.user.position=position
     // this.center={'lat':parseFloat(position.lat),'lng':parseFloat(position.lng)}
     //this.fitBounds()
    }.bind(this));

    finance.getCurrency(this)

    this.fetchPage()
  },
  mounted(){
		this.links = this.loadAll();
  }

}
</script>
<style lang="scss">

$blue: #6d9ee1;
$shadow1: 0 0 7px 0 rgba(0, 0, 0, 0.33);

*{
 font-family: 'PT Sans', sans-serif;
}

.button{
  background-color: $blue;
  color: #e5e5e5;
  text-align: center;
  padding: 10px;
  border-radius: 4px;
  &:hover{
    color: #fff;
  }
}
.voter-list{

}
.el-icon-loading{
  text-align: center;
  vertical-align: middle;
  display: block!important;
  margin-top: 50%!important;
}

body, html{
    padding: 0;
    margin: 0;
}
/*Microframework*/
.one-fourth{
  width:25%;
  display: inline-block;
  float: left;
}
.half{
  width:50%;
  display: inline-block;
  float: left;
}
.full{
  width: 100%;
  display: block;
  clear: both;
  a{
    color: #000!important;
    &:hover{
      text-decoration: none!important;
    }
  }
  h2{
    &:hover{
      text-decoration: underline!important;
    }
  }
}
.table {
  >*{
    display: table-cell;
  }
  display: table;
  width:100%;
}
.infopanel{
  >*{
    text-align: center;
  }
}
/*end Microframework*/



/*
.el-dropdown {

    color: #fff!important;
    font-size: 14px;
    padding: 10px;
}
 */
.page-list{
  display: block;
  width: 100%;
  padding: 23px;
  box-sizing: border-box;
  .profile{
    background: #fff;
    display: block;

    border-radius: 10px;
    margin-bottom: 35px;
    .username{
      color:#485465;
      font-size: 26px;
      text-align: center;
    }
  }
  .author_avatar{
    width: 200px;
    height: 200px;
    border-radius: 200px;
    display: block;
    margin: auto;
  }
  .self_blog_view_buttons{
    text-align: center;
    margin: 10px;
    display: inline-block;
    width: 100%;
  }
  .article{
    display: inline-block;
    clear: both;
    box-shadow: 0px 0px 43px rgba(0, 0, 0, 0.1);
    border-bottom: 2px solid #eee;
    cursor: pointer;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 27px;
    margin-top: 71px;
    background-color: #fff;
    h1{
      padding: 0;
      margin: 0 0 5px 0;
      font-size: 24px;
    }
    a{
      /* color: inherit; */
    }
    .body{
      min-height: 100px;
    }
    .post-preview{
      box-shadow: $shadow1;
      border-radius: 5px;
      width: 95%;
      box-sizing: border-box;
      padding: 10px;
      min-height: 150px;
      background-color: #fff;
      top: -55px;
      margin: -72px auto 11px auto;
      clear: both;
      .post-info{
       display: table;
       position: relative;
       background: #fff;
       width: 100%;
       border-radius: 10px 10px 0 0;
       width: 104%;
       bottom: -2px;
       margin-left: -2%;
        img{
          width: 50px;
          height: 50px;
          display:block;

        }
        .avatar{
          display: table-cell;
          width: 76px;
          >img{
            border-radius: 50px;
            margin: 5px auto 0px auto;
          }
        }
        .head{
          padding: 5px 10px;
          box-sizing: border-box;
          vertical-align: top;
          display:table-cell;
        }
        .full{
          display: table-row;

        }
        h4{
          margin: 0 0 10px 0!important;
        }
      }
      .comments{
        font-size: 12px;
      }

    }
    .bottom{
      display: block;
      width: 94%;
      margin: 25px auto;
      min-height: 40px;
      box-sizing: border-box;
      font-size: 13px;
      a{
        width: 100%;
        text-align: center;
        display: block;
      }
      .button{
        font-size: 16px;
      }
    }
    .comments-wrapper {
      .load-more{
        border-radius: 6px;
        text-align: center;
        background-color: #e3e8ef;
        font-size: 14px;
        font-weight: normal;
        letter-spacing: -0.3px;
        color: #5d7394;
        width: 90%;
        margin: 0 auto 20px auto;
        display: block;
        padding: 10px;

        &:hover{
          font-weight: bold;
        }
      }

    }



    .post-image{
      width: 100%;
      height: 400px;
      object-fit: cover;
      border-radius: 5px 5px 0 0;
      margin: 0 auto 10px auto;
    }
    .dummy-image{
     display: inline-block;
     width: 20%;
     height: 140px;
     background-size: contain;
     background-repeat: no-repeat;
     background-position: 50%;
    }
    >img{
     height: auto;
     vertical-align: middle;
     width: 90%;
     margin: 10px auto;
     display: block;
    }

    img[lazy*="error"], img[lazy*="loading"]{
      display: none;
    }
    img[lazy*="loaded"] + .dummy-image{
      display: none;
    }
    .content{
      float: right;
      display: inline-block;
      width: 80%;
      overflow: hidden;
      height: auto;
    }
  }

  a{
    color: #337ab7;
    text-decoration: none;
    &:hover{
      text-decoration: underline;
    }
  }
}


article
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0
}
</style>

<style lang="scss" scoped>
.voter-list{
 width: 48%;
    position: fixed!important;
    left: 52%!important;
    border: 1px solid #ccc;
    box-sizing: border-box;
    top: 50%!important;

}
.stat{
  display: inline-block;
  float: left;
  box-sizing: border-box;
  padding-right: 15px;
  text-align: right;
  width: 20%;
}
.voters{
  display: inline-block;
  float: left;
  box-sizing: border-box;
  height: 40px;
  width: 80%;
  border:1px dotted #aaa;
  overflow: scroll;
  &:hover{
   position: relative;
   top: 0;
   right: 0;
   border: 1px solid #eaeaea;
   height: 200px;
   background-color: #ffffff;
   margin-top: -160px;
   box-shadow: 1px 1px 20px rgba(0,0,0,0.2) inset;
   padding: 2px;
   border-radius: 10px…;
  }

}
.voter{
  display: inline-block!important;
  float: left!important;
  margin-left: 5px;
  &:hover{
    background-color: #ccc;

  }
}
  .vue-map-container{
    left: 0;
    top: 0;
    position: fixed;
    z-index: 0;
    width: 100%;
    height: 100vw;
  }
  .wrapper{
    display: block;
    z-index: 10;
    position: relative;
    width: 38%;
    padding-left: 3%;

  }
  .loader{
   height: 100vw;
   display: block;
   z-index: 10;
   width: 35%;
   text-align: center;
   vertical-align: middle;
   position: fixed;
  }

  .search-box{
    position: fixed;
   left: 41%;
   width: 57%;
    top: 80px;
    z-index: 10;
    input{
      width: 100%;
    }
    .el-autocomplete, .el-dropdown {

        width: 100%;
    }
  }
</style>
