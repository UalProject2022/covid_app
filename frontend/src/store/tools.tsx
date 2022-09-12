export async function fetchData(url: string) {
  const requestOptions: RequestInit = {
    method: 'GET',
    redirect: 'follow',
  }

  try {
    const response = await fetch(url, requestOptions);
    return response.ok ? response.json() : []
  } catch (err) {
    console.log(err);
    return [];
  }

}
