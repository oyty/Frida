import frida, sys


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


jscode = """
Java.perform(function () {
    // Function to hook is defined here
    //所有响应
    var Response = Java.use('mtopsdk.network.domain.Response');
    Response.$init.overload('mtopsdk.network.domain.Response$Builder').implementation = function() {
        //PrintStack()
        console.log("Response " + arguments[0].body)
        var ret = this.$init.apply(this, arguments);
        //all request
        console.log("Response " + this.toString())
        return ret;
    };
    
    //所有请求
    var RequestBuilder = Java.use('mtopsdk.network.domain.Request$Builder');
    RequestBuilder.build.overload().implementation = function() {
        //PrintStack()
        var ret = this.build.apply(this, arguments);
        //all request
        console.log("RequestBuilder " + ret.toString())
        return ret;
    };
    
    //所有请求
    var ANetworkCallImpl = Java.use('mtopsdk.network.impl.ANetworkCallImpl');
    ANetworkCallImpl.$init.overload('mtopsdk.network.domain.Request', 'android.content.Context').implementation = function() {
        //PrintStack()
        console.log('ANetworkCallImpl ' + arguments[0])
        var ret = this.$init.apply(this, arguments);
    
        return ret;
    };
    
    //所有请求url
    var AbstractNetworkConverter = Java.use(
        'mtopsdk.mtop.protocol.converter.impl.AbstractNetworkConverter'
    );
    AbstractNetworkConverter.buildBaseUrl.overload(
        'mtopsdk.framework.domain.MtopContext',
        'java.lang.String',
        'java.lang.String'
    ).implementation = function() {
        console.log("buildBaseUrl "+arguments[1]+' '+arguments[2])
    
        var ret = this.buildBaseUrl.apply(this, arguments);
        //url
        console.log("buildBaseUrl "+ret)
        return ret;
    };
    
    // 禁用spdy协议
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.setGlobalSpdySslSwitchOpen.overload().implementation = function() {
        var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        console.log('isGlobalSpdySwitchOpenl ' + ret)
    
        return false;
    };

    
});
"""

process = frida.get_usb_device().attach('cn.damai')
script = process.create_script(jscode)
# script.on('message', on_message)
print('[*] Running CTF')
script.load()
sys.stdin.read()
