// 7549245454
// https://www.myvi.in/bin/vodafoneideadigital/servlet/Etopup/pack.0020.json

var validationMessage = "";
var orcNumberEntered = false;
var compareMobFlag = false;
var mobNumber, subscriberType, status, brand, lob, customertype, vodaCircleName;

function handleSpecialChars(encryptedNumber) {
    return encryptedNumber.replace(/[+]/g, "%2B");
}

var encryptVars = function(mobNumber) {
    var salt = CryptoJS.lib.WordArray.random(128 / 8);
    var iv = CryptoJS.lib.WordArray.random(128 / 8);
    var secretPassPhrase = CryptoJS.lib.WordArray.random(128 / 8);
    var key128Bits = CryptoJS.PBKDF2(secretPassPhrase.toString(), salt, {
        keySize: 128 / 32
    });
    var key128Bits100Iterations = CryptoJS.PBKDF2(secretPassPhrase.toString(), salt, {
        keySize: 128 / 32,
        iterations: 100
    });
    var encryptedNumber = CryptoJS.AES.encrypt(mobNumber, key128Bits100Iterations, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return {
        salt: salt,
        iv: iv,
        secretPassPhrase: secretPassPhrase,
        encryptedNumber: handleSpecialChars(encryptedNumber.toString())
    };
}

var reccP;
function validNumberF(mobNumber) {
    var object = {};
    var requestParamsJson = {};
    mobNumber = $("#orc-mobile").val();
    requestParamsJson["mobNumber"] = mobNumber;
    requestParamsJson["isCouponIdentifier"] = "COUPON";
    requestParamsJson["YbbCheck"] = "YbbCheck";
    var encVals = encryptVars(JSON.stringify(requestParamsJson));
    object['params'] = encVals.encryptedNumber.toString();
    object['sl'] = encVals.salt.toString();
    object['algf'] = encVals.iv.toString();
    object['sps'] = encVals.secretPassPhrase.toString();
    $.ajax({
        url: "https://www.myvi.in/bin/selected/prepaidrechargevalidation",
        type: 'POST',
        data: 'mobile=' + JSON.stringify(object),
        asyn: false,
        beforeSend: function() {},
        success: function(result) {
            var json_obj = $.parseJSON(result);
            if (json_obj.downtimecircle) {
                if (json_obj.subscriberType.toUpperCase() == "PREPAID" && json_obj.downtimecircle == "true") {
                    json_obj.STATUS = "SUCCESS";
                }
            }
            console.log(json_obj);
        },
        error: function(xhr, textStatus) {
            if (xhr.status == 401 || xhr.status == 307) {
                var msg = "You have exceeded the maximum attempts for Number Entry. Please try after some time.";
                // vodafoneMobileEncryption(mobNumber, "NOT_FOUND", "NOT_FOUND", "MAX_ATTEMPTS", "NOT_FOUND");
                console.log(msg);
            }
        },
        complete: function() {
            $.get("https://www.myvi.in/bin/vodafoneideadigital/servlet/Etopup/pack."+circleId+".json", function(e){
                console.log(e);
            });
        }
    });
}