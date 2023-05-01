var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        is_login:true,
        username:'',
        // avatar:''
    },
    mounted(){
        this.username=getCookie('username');
        this.is_login=getCookie('is_login');
        // this.avatar=this.host + getCookie('avatar')
    },
    methods: {
        //显示下拉菜单
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
        on_submit(){

        },
        // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
        // generate_avatar_url: function () {
        //     // 设置页面中图片验证码img标签的src属性
        //     this.avatar = this.host + "/imagecode/?uuid=" + this.uuid;
        // },
    }
});
