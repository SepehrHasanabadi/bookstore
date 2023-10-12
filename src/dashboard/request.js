export function getRequest(axios, auth, url, params) {
  return axios({
    url,
    method: 'get',
    headers: {
      "Authorization": auth.strategy.token.get()
    },
    params,
  });
}
export function postRequest(axios, auth, url, data) {
  return axios({
    url,
    method: 'post',
    data,
    headers: {
      "Authorization": auth.strategy.token.get()
    }
  });
}

export function putRequest(axios, auth, url, data) {
  return axios({
    url,
    method: 'put',
    data,
    headers: {
      "Authorization": auth.strategy.token.get()
    }
  });
}