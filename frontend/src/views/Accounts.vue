<template>
  <div>
    <b-container>

      <b-row align-h="center">
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

      <b-row align-h="center">
        <b-col cols="12">
          <b-table striped hover small :items="accounts" :fields="fields">
            <template #cell(action)="row">
              <b-button size="sm" @click="onManage(row.item)">
                Manage
              </b-button>
            </template>
          </b-table>
        </b-col>
      </b-row>

      <!-- The modal -->
      <b-modal ref="manage_account_modal" hide-footer title="Manage account">
        <b-container>

          <b-row align-v="center">
            <b-col cols="12">
              <div class="d-block text-center mb-3">
                <h3>{{current_account.email}}</h3>
              </div>
            </b-col>
          </b-row>

          <b-row align-v="center" class="my-3 mx-3">
            <b-col cols="3" align-self="start">
              Status: {{current_account.status}}
            </b-col>
            <b-col cols="7">
              <b-form-input id="range-1" v-model="current_account.status" type="range" min="0" max="5"></b-form-input>
            </b-col>
            <b-col cols="2" class="ml-auto">
              <b-button size="sm" @click="put_account_status">
                Save
              </b-button>
            </b-col>
          </b-row>

          <b-row align-v="center" class="my-3 mx-3">
            <b-col cols="3" align-self="start">
              User:
            </b-col>
            <b-col cols="4">
              <b-form-select v-model="current_user_id" :options="users"></b-form-select>
            </b-col>
            <b-col cols="2">
              <b-button size="sm" @click="put_account_connect">
                Connect
              </b-button>
            </b-col>
            <b-col cols="2" class="ml-2">
              <b-button size="sm" @click="put_account_disconnect">
                Disconnect
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

const GET_ACCOUNTS = "/admin/accounts/";
const PUT_ACCOUNT_STATUS = "/admin/accounts/status/";
const PUT_ACCOUNT_CONNECT = "/admin/accounts/connect/";
const PUT_ACCOUNT_DISCONNECT = "/admin/accounts/disconnect/";

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

        action: 'Connect',

        current_account: {},
        current_user_id: '',

        fields: ['email', 'status', 'owner_id', 'action'],
        accounts: [{
          "account_id": '1',
          "owner_id": "3456u7i8o9lu",
          "email": "string@we.oi",
          "credentials": {},
          "status": 0,
          "error_message": ""
        },
        {
          "account_id": '2',
          "owner_id": "luikyutjrew4",
          "email": "123@qwe.io",
          "credentials": {},
          "status": 0,
          "error_message": ""
        },
        {
          "account_id": '3',
          "owner_id": ",khmjngbrgwet45yr",
          "email": "442xcv@dd.com",
          "credentials": {},
          "status": 0,
          "error_message": ""
        },
        {
          "account_id": '4',
          "owner_id": "23q321",
          "email": "ex@pop.de",
          "credentials": {},
          "status": 0,
          "error_message": ""
        }],

        dummy_users: [{user_id: '12322222qqq', email: 'Dickerson@mail.oi', level: 1},
            {user_id: '23q321', email: 'Larsen@gmail.com', level: 3},
            {user_id: '132we23', email: 'Geneva@ya.ru', level: 2},
            {user_id: '5tgvw3', email: 'Jami@mycomp.com', level: 5}],
        
        users: [],
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
      onManage(account) {
        this.$set(this, 'current_account', account)
        console.log(this.current_account)
        this.get_users()
        this.$refs["manage_account_modal"].show()
      },
    async get_accounts() {
        let path = GET_ACCOUNTS
        axios
            .get(path)
            .then(res => {
                let r = res.data
                console.log(res)
                this.show_notification(r)
                r = JSON.parse(r)
                
                this.$set(this, 'accounts', r)
            })
            .catch(error => {
                this.show_notification(error, 'danger')
            })
    },
    async put_account_status() {
        let path = PUT_ACCOUNT_STATUS
        let data = new FormData()
        data.append("account", this.current_account)

        axios
            .put(path, data)
            .then(res => {
                console.log(res)
            })
            .catch(error => {
                this.show_notification(error, 'danger')
            })
        
        await this.get_accounts()
        this.$refs["manage_account_modal"].hide()
    },
    async put_account_connect() {
        let path = PUT_ACCOUNT_CONNECT
        let data = new FormData()
        data.append("account_id", this.current_account)
        data.append("user_id", this.current_user_id)

        axios
            .put(path, data)
            .then(res => {
                console.log(res)
            })
            .catch(error => {
                this.show_notification(error, 'danger')
            })
        
        await this.get_accounts()
        this.$refs["manage_account_modal"].hide()
    },
    async put_account_disconnect() {
        let path = PUT_ACCOUNT_DISCONNECT
        let data = new FormData()
        data.append("account_id", this.current_account)
        data.append("user_id", this.current_user_id)

        axios
            .put(path, data)
            .then(res => {
                console.log(res)
            })
            .catch(error => {
                this.show_notification(error, 'danger')
            })
        
        await this.get_accounts()
        this.$refs["manage_account_modal"].hide()
    },
    async get_users() {
        let path = GET_USERS
        axios
            .get(path)
            .then(res => {
                let r = res.data
                console.log(r)

                let users = JSON.parse(r)
                this.transform_users(users)
            })
            .catch(error => {
                this.show_notification(error, 'danger')
            })

        this.transform_users() // dummy
    },
    transform_users() {
      let users = this.dummy_users // dummy users
      this.$set(this, 'current_user_id', '') // refresh current_user_id

      if(Array.isArray(users) && users.length > 0) {

        try {
          // try to get user_id of current account
          let attached_user_id = users.find(user => user.user_id == this.current_account.owner_id).user_id 
          this.$set(this, 'current_user_id', attached_user_id)
          console.log('current_user_id: ' + this.current_user_id)

        } catch(err) {
          console.log(err)
          console.log("account don't has owner_id or users don't contain this oner_id")
        }
        
        // transform users to readable format for select
        users = users.map(user => {
          return {value: user.user_id, text: user.user_id}
        })
        this.$set(this, 'users', users)
        console.log(this.users)
      }
    }
  },
  
  async mounted() {
    await this.get_accounts()
  }
};
</script>
<style lang="scss">

</style>
