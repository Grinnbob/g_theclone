<template>
  <div>
    <b-container>

      <b-row align-v="center">
        <b-col cols="4" class="ml-auto">
          <b-alert
            :show="dismissCountDown"
            dismissible
            :variant="notification_type"
            @dismissed="dismissCountDown=0"
            @dismiss-count-down="countDownChanged"
            >
            {{ notification_text }}
          </b-alert>
        </b-col>
      </b-row>

      <b-row align-v="center">
        <b-col cols="12">
          <b-table striped hover small :items="users" :fields="fields">
            <template #cell(action)="row">
              <b-button size="sm" @click="onChooseUser(row.item)">
                Change level
              </b-button>
            </template>
          </b-table>
        </b-col>
      </b-row>

      <!-- The modal -->
      <b-modal ref="change_user_level_modal" hide-footer title="Change user level">
        <b-container>
          <b-row align-v="center">
            <b-col cols="12">
              <div class="d-block text-center mb-3">
                <h3>{{current_user.user_id}}</h3>
              </div>
            </b-col>
          </b-row>
          <b-row align-v="center">
            <b-col cols="3" align-self="start">
              Level: {{ current_user.level }}
            </b-col>
            <b-col cols="7">
              <b-form-input id="range-1" v-model="current_user.level" type="range" min="0" max="5"></b-form-input>
            </b-col>
            <b-col cols="2" class="ml-auto">
              <b-button size="sm" @click="put_user_level">
                Save
              </b-button>
            </b-col>
          </b-row>
        </b-container>
      </b-modal>

    </b-container>

  </div>
</template>
<script>
import axios from '@/api/axios-auth';

const GET_USERS = "/admin/users/";
const PUT_USER_LEVEL = "/admin/users/level/";

export default {
  components: {
  },
 data() {
    return {
      // Notifications
        dismissSecs: 10,
        dismissCountDown: 0,
        notification_text: '',
        notification_type: 'warning',

        current_user: {},

        fields: ['user_id', 'level', 'action'],
        users: [{user_id: '12322222qqq', email: 'Dickerson@mail.oi', level: 1},
            {user_id: '23q321', email: 'Larsen@gmail.com', level: 3},
            {user_id: '132we23', email: 'Geneva@ya.ru', level: 2},
            {user_id: '5tgvw3', email: 'Jami@mycomp.com', level: 5}],
    };
  },
  methods: {
      countDownChanged(dismissCountDown) {
        this.$set(this, 'dismissCountDown', dismissCountDown)
      },
      show_notification(text, type='warning') {
          this.$set(this, 'notification_text', text)
          this.$set(this, 'notification_type', type)
          this.$set(this, 'dismissCountDown', this.dismissSecs)
      },
      onChooseUser(user) {
        this.$set(this, 'current_user', user)
        console.log(this.current_user)
        this.$refs["change_user_level_modal"].show()
      },
    async get_users() {
        let path = GET_USERS
        axios
            .get(path)
            .then(res => {
                let r = res.data
                console.log(res)
                this.show_notification(r)
                r = JSON.parse(r)
                
                this.$set(this, 'users', r)
            })
            .catch(error => {
                this.show_notification(error, 'danger')
            })
    },
    async put_user_level() {
        let path = PUT_USER_LEVEL
        let data = new FormData()
        data.append("user_id", this.current_user.user_id)
        data.append("level", this.current_user.level)

        axios
            .put(path, data)
            .then(res => {
                console.log(res)
            })
            .catch(error => {
                this.show_notification(error, 'danger')
            })
        
        await this.get_users()
        this.$refs["change_user_level_modal"].hide()
    },
  },
  
  async mounted() {
    await this.get_users()
  }
};
</script>
<style lang="scss">

</style>
