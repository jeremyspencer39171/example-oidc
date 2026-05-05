<script lang="ts">
  import { onMount } from 'svelte';

  let code: string | null = null;
  let state: string | null = null;
  let redirect_uri: string | null = null;
  let client_id: string | null = null;
  let client_secret: string | null = null;
  let tokens: any = null;

  onMount(async () => {
    const params = new URLSearchParams(window.location.search);
    code = params.get('code');
    state = params.get('state');
    redirect_uri = params.get('redirect_uri');
    client_id = params.get('client_id');
    client_secret = params.get('client_secret');

    if (!code) return;

    const body = new URLSearchParams();
    body.set('grant_type', 'authorization_code');
    body.set('code', code);
    body.set('redirect_uri', redirect_uri);
    body.set('client_id', client_id);
    body.set('client_secret', client_secret);

    const res = await fetch('https://api.hostname:81/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });

    tokens = await res.json();
  });
</script>

<main>
  <h1>Callback</h1>
  {#if tokens}
    <pre>{JSON.stringify(tokens, null, 2)}</pre>
  {:else}
    <p>Waiting for tokens...</p>
  {/if}
</main>
