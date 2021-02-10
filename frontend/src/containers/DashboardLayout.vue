<template>
  <div>
    <div>
      <b-navbar toggleable="md" type="light" variant="light">
        <b-navbar-brand href="#"></b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item href="/users">Users</b-nav-item>
            <b-nav-item href="/accounts">Accounts</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <div class="mx-4 my-4">
      <router-view></router-view>
    </div>
  </div>
</template>
<script>

</script>