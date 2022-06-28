import axios from "axios";
import { UserModel } from "../models/User";


class AuthService {
  setUserInLocalStorage(data: UserModel) {
    console.log(data);


    localStorage.setItem("user", JSON.stringify(data));
    // localStorage.setItem("token", JSON.stringify(data));

  }

  async login(email: string, password: string): Promise<UserModel> {
    const response = await axios.post("http://192.168.1.106:8000/auth/jwt/create/", { email, password });
    console.log(response.data)
    if (response.data) {
      //return response.data;
      const resp = await axios.get("http://192.168.1.106:8000/auth/users/me/", { headers: { Authorization: "JWT " + response.data.access } })
      if (resp.data) {
        console.log(resp.data)
        this.setUserInLocalStorage(resp.data);
        localStorage.setItem("token", JSON.stringify(response.data));
        // this.setUserInLocalStorage(response.data);
        return resp.data;
      }
    }
    return response.data.access;
  }

  logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("token");

  }

  getCurrentUser() {
    const user = localStorage.getItem("user")!;
    const token = localStorage.getItem("token")!;


    return JSON.parse(user);
  }
}

export default new AuthService();