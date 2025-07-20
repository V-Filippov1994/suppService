import axios from "axios";

let serverUrl = '';

if (window.location.hostname === 'localhost') {
  serverUrl = 'http://localhost:8000';
}

export let serverBaseUrl = `${serverUrl}/api/`;


export const api = async (method, url, data) => {
  let resp;
  try {
    resp = await axios[method](serverBaseUrl + url, data);
  }  catch (e) {
    return { data: e.response.data.detail };
  }
  return resp
}