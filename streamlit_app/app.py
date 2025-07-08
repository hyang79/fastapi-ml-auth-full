import streamlit as st, requests

def main():
    st.title("FastAPI ML + Auth Demo")
    if "access" not in st.session_state:
        uname = st.text_input("Username"); pw = st.text_input("Password", type="password")
        if st.button("Login"):
            r = requests.post("http://localhost:8000/token", json={"username":uname,"password":pw})
            if r.status_code==200:
                st.session_state.access = r.json()["access_token"]
                st.success("Logged in!")
            else: st.error("Login failed")
    else:
        inp = st.text_input("Features (4 nums comma)")
        if st.button("Predict"):
            f = list(map(float, inp.split(",")))
            r = requests.post("http://localhost:8000/predict", headers={"Authorization":f"Bearer {st.session_state.access}"}, json={"features":f})
            if r.status_code==401:
                st.error("Unauthorized")
            else: st.success(f"Result: {r.json()['result']}")
        if st.button("Logout"):
            requests.post("http://localhost:8000/logout", json={"refresh_token":st.session_state.access})
            del st.session_state.access
            st.info("Logged out")

if __name__=="__main__":
    main()