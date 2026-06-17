<script>
  import { Router } from "svelte-spa-history-router";
  import Login from "./routes/login.svelte";

  let routes = [
    { path: "/login", component: Login },
  ];
</script>

<section id="center">
  <section id="spacer"></section>
  <Router {routes} />
</section>
