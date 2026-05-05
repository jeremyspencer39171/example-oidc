<script lang="ts">
  import { onMount } from 'svelte';

  let username = '';
  let password = '';

  let response_type = '';
  let client_id = '';
  let redirect_uri = '';
  let scope = '';
  let state: string | null = null;

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    response_type = params.get('response_type') || 'code';
    client_id = params.get('client_id') || '';
    redirect_uri = params.get('redirect_uri') || '';
    scope = params.get('scope') || 'openid profile email';
    state = params.get('state');
  });
</script>

<main>
  <h1>Sign in</h1>
<form method="POST" action="https://api.hostname:81/login">
  <input type="hidden" name="response_type" value={response_type} />
  <input type="hidden" name="client_id" value={client_id} />
  <input type="hidden" name="redirect_uri" value={redirect_uri} />
  <input type="hidden" name="scope" value={scope} />
  {#if state}
    <input type="hidden" name="state" value={state} />
  {/if}

  <label>Email <input type="email" name="username" required /></label>
  <label>Password <input type="password" name="password" required /></label>

  <button type="submit">Login</button>
</form>
</main>
