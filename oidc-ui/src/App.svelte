<script>
  import { Router } from "svelte-spa-history-router";
  import svelteLogo from "./assets/svelte.svg";
  import viteLogo from "./assets/vite.svg";
  import heroImg from "./assets/hero.png";
  import Counter from "./lib/Counter.svelte";
  import Login from "./routes/login.svelte";

  let routes = [
    { path: "/login", component: Login },
  ];
</script>

<section id="center">
  <section id="spacer"></section>
  <Router {routes} />
</section>

<section id="center">
  <div class="hero">
    <img src={heroImg} class="base" width="170" height="179" alt="" />
    <img src={svelteLogo} class="framework" alt="Svelte logo" />
    <img src={viteLogo} class="vite" alt="Vite logo" />
  </div>
  <div>
    <h1>Get started</h1>
    <p>Edit <code>src/App.svelte</code> and save to test <code>HMR</code></p>
  </div>
  <Counter />
</section>
