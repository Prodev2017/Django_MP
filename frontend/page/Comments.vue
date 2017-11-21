<template>
<el-card class="box-card comment_list">
  <router-link :to=" '/'+ model.author">
   <img class="avatar" :src="model.author_avatar" alt=""> <b>{{model.author}}</b>
  </router-link>
  {{model.created_at | formatDate }}  {{model.created_at.replace('T',' ').replace('Z',' ') }}
  <div v-html="$options.filters.markdown(model.body)"></div>
<!--   <el-popover
        ref="popover1"
        placement="top-start"
        title="Понравилось"
        width="200"
        trigger="hover"
        :content="model.voters">
  </el-popover>
  <el-button v-popover:popover1>
    поддержали:
  </el-button> -->


  <i class="fa fa-plus" v-if="!new_comment && user.has_public_key" v-on:click="showText()">ответить</i>
  <div v-if="this.textarea_visible" >
    <textarea class="new_comment_textarea" cols="30" rows="10" v-model="new_comment" placeholder="Добавьте комментарий"></textarea>
    Просмотр
    <el-card  v-html="$options.filters.markdown(new_comment)" class="box-card"></el-card>
    <br>
    <el-button type="primary" v-on:click="addComment(model)" v-if="new_comment" size="mini">Добавить комментарий</el-button>
    <i class="fa fa-close" v-if="new_comment" v-on:click="new_comment=null">отменить</i>
  </div>
  <ul v-if="isFolder">
    <comments
      class="item"
      v-for="model in sortedComments"
			:key="null"
      :model="model"
      >
    </comments>
  </ul>
</el-card>
</template>

<script>
import Vue from 'vue'
import router from '../main.js'
import auth from '../auth'
export default {
  name: 'Comments',
  props: {
      model: {
        author:null,
        body:null
      }
  },
  data: function () {
    return {
      // open: false,
      textarea_visible: false,
      new_comment: null,
      user:auth.user
    }
  },

  computed: {
    isFolder: function () {
      return this.model.children &&
        this.model.children.length
    },
    isRoot:function () {
      return !this.model.name
    },

    sortedComments: function() {
        this.model.children.sort( ( a, b) => {
            return new Date(a.date) - new Date(b.date);
        });
        return this.model.children;
    }

  },
  methods: {
    showText (){
      this.new_comment=null
      this.textarea_visible=!this.textarea_visible

    },
    addComment (incoming_comment){
      this.$http.post(this.$route.path, {
        'comment':this.new_comment,
        'parent_comment_id':incoming_comment.id
      }, (data) => {
        if (data.status=="success"){
          // this.$message({
          //     type: 'success',
          //     message: 'ком принят'
          // })
          this.model.children.push({
            author:auth.user.username,
            body:this.new_comment,
            id:data.id,
            children:[]
          })
          this.new_comment=null
          this.textarea_visible=false


          /*
          if (params.upvote){
            this.page.voters.push(auth.user.username)
          }
          else{
            this.page.voters.splice(this.page.voters.indexOf(auth.user.username),1)
          }
          */
        }
        else{
          this.$message({
              type: 'error',
              message: 'comment error: '+JSON.stringify(data)
          })
        }
      })
    }
  },
  created: function () {
  }
}

</script>

<style lang="scss" scoped>
.box-card{
  margin: 10px 0;
  padding: 0 10px;
}
.new_comment_textarea{
  width:100%;
}
.page > .comments{
  box-shadow: none;
  border: none;
}
.avatar {
  width: 30px;
  height: 30px;
  border-radius: 30px;
}
</style>
