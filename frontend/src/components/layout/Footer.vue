<template>
    <div class="footer">
        <!-- <div class="row mx-5 pt-4"> -->
            <!-- <div class="col col-md-4 px-1 left"> -->
            <div class="left">
                <router-link exact-active-class="link-home-footer" class="link-home-footer" to="/">
                    <img class="img" src="~@/assets/Logo.png">
                    <!-- <img class="img" src="~@/assets/atp.png">
                    <span class="name-group-footer">BIOMODELING</span> -->
                </router-link>
            </div>
            <!-- <div class="col col-md-4 px-5 center"> -->
            <div class="center">
                <h5 class="mb-3"><strong>Social links</strong></h5>
                <p class="mb-1"><i class="bi bi-twitter mx-2"></i>Twitter</p>
                <p class="mb-1"><i class="bi bi-linkedin mx-2"></i>Linkedin</p>
            </div>
            <!-- <div class="col col-md-4 px-5 right"> -->
            <div class="right">
                <h5 class="mb-2"><strong>Contacts</strong></h5>
                <span style="font-size: 12px">
                    <p class="ms-2" style="margin-bottom:1px;">Viale Regina Elena, 291</p>
                    <p class="ms-2" style="margin-bottom:1px;">00161 Roma</p>
                    <p class="ms-2" style="margin-bottom:1px;">Italy</p>
                    <p class="ms-2">email@example.com</p>
                </span>
                <!-- <span class="mb-1">Viale Regina Elena, 291</span>
                <span class="mb-1">00161 Roma</span>
                <span class="mb-1">Italy</span> -->
            </div>
        <!-- </div> -->
        <!-- <router-link class="logo" to="/" @click="current = 0" >
            <img class="img" src="~@/assets/atp.png">
            <span style="font-weight: bold; font-size: 30px; vertical-align: top;">ROBiOCOmP</span>
        </router-link> -->
    </div>
</template>

<script>
// export default {
//     name: 'Footer'
// }
</script>

<style scoped lang="scss">
@media screen and (min-width: 670px) {

    .footer {
        background-color: #38444a;
        position: relative;
        bottom: 0;
        width: 100%;
        height: 150px;
        box-shadow: 0px 0 8px rgba(0, 0, 0, 0.8);
        color: #f5f5f5;
    }

    .left {
        width: 40%;
        float: left;
        margin: 20px;
    }

    .center {
        width: 20%;
        float: left;
        margin: 20px;
    }

    .right {
        width: 20%;
        float: right;
        margin: 20px 20px 0 20px;
    }
    
}


@media screen and (max-width: 669px) {

    .footer {
        background-color: #38444a;
        position: relative;
        bottom: 0;
        width: 100%;
        height: 400px;
        box-shadow: 0px 0 8px rgba(0, 0, 0, 0.8);
        color: #f5f5f5;
    }

    .left {
        width: 100%;
        padding: 20px;
        align-content: center;
        text-align: center;
    }

    .center {
        width: 100%;
        padding: 20px 0 0 0;
        align-content: center;
        text-align: center;
    }

    .right {
        width: 100%;
        padding: 20px 20px 0 20px;
        align-content: center;
        text-align: center;
    }

}

// .footer {
//     /* overflow: hidden; */
//     background-color: #38444a;
//     position: relative;
//     /* margin-top: auto; */
//     /* margin-top: -150px; */
//     /* left: 0; */
//     bottom: 0;
//     width: 100%;
//     height: 150px;
//     /* z-index: 99; */
//     box-shadow: 0px 0 8px rgba(0, 0, 0, 0.8);
//     color: #f5f5f5;
// }

.logo {
    text-decoration: none;
    color: #f5f5f5;
}

.img {
    width: auto;
    height: 75px;
}

.link-home-footer {
    text-decoration: none;
    color: #fff;
    background-color: lightgray;
    // padding: 20px;
    padding: 40px 8px 40px 8px;
    border-radius: 8px;
}
.name-group-footer {
    font-weight: bold; 
    font-size: 30px; 
    vertical-align: top;
}

.router-link-exact-active {
    padding: 0px;
}
</style>