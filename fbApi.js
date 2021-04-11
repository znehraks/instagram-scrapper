// facebook login
exports.facebookLogin = function(req, res) {
    var fields = config.loginFaceBook.fbFields;
    var accessTokenUrl = config.loginFaceBook.fbAccessTokenUrl;
    var graphApiUrl = config.loginFaceBook.fbGraphApiUrl + fields.join(',');
    var params = {
        code: req.body.code,
        client_id: req.body.clientId,
        client_secret: config.loginFaceBook.fbClientSecret,
        redirect_uri: req.body.redirectUri
    };

    // Step 1. Exchange authorization code for access token.
    request.get({
        url: accessTokenUrl,
        qs: params,
        json: true
    }, function(err, response, accessToken) {
        console.log('Exchange authorization code err::', err);
        console.log('Exchange authorization code accessToken::', accessToken);
        if (response.statusCode !== 200) {
            return res.status(500).send({
                message: accessToken.error.message
            });
        }

        // Step 2. Retrieve profile information about the current user.
        request.get({
            url: graphApiUrl,
            qs: {
                access_token: accessToken.access_token,
                fields: fields.join(',')
            },
            json: true
        }, function(err, response, profile) {
            console.log('Retrieve profile information err::', err);
            console.log('Retrieve profile information::', profile);
            if (response.statusCode !== 200) {
                return res.status(500).send({
                    message: profile.error.message
                });
            }
            if (req.header('Authorization')) {
                console.log('req header Authorization', req.header('Authorization'));
            } else {
                var socialEmail;
                if (profile.email) {
                    socialEmail = profile.email;
                } else {
                    socialEmail = profile.id + '@facebook.com';
                }

                // Step 3. Create a new user account or return an existing one.
                UserModel.findOne({
                    email: socialEmail
                }, function(err, existingUser) {
                    if (existingUser) {
                        AppClientModel.findOne({
                            _id: config.auth.clientId
                        }, function(err, client) {
                            if (!err) {
                                var refreshToken = generateToken(existingUser, client, config.secrets.refreshToken);
                                var rspTokens = {};
                                rspTokens.access_token = generateToken(existingUser, client, config.secrets.accessToken, config.token.expiresInMinutes);
                                var encryptedRefToken = cryptography.encrypt(refreshToken);
                                var token = {
                                    clientId: client._id,
                                    refreshToken: refreshToken
                                };

                                UserModel.update({
                                    _id: existingUser._id
                                }, {
                                        $push: {
                                            'tokens': token
                                        }
                                    }, function(err, numAffected) {
                                        if (err) {
                                            console.log(err);
                                            sendRsp(res, 400, err);
                                        }
                                        res.cookie("staffing_refresh_token", encryptedRefToken);
                                        sendRsp(res, 200, 'Success', rspTokens);
                                    });
                            }
                        });
                    }
                    if (!existingUser) {
                        var userName = profile.first_name + ' ' + profile.last_name;
                        var newUser = new UserModel({
                            name: userName,
                            img_url: 'https://graph.facebook.com/' + profile.id + '/picture?type=large',
                            provider: 2, //2: 'FB'
                            fb_id: profile.id,
                            email_verified_token_generated: Date.now()
                        });
                        log.info("newUser", newUser);
                        newUser.save(function(err, user) {
                            if (!err) {
                                var refreshToken = generateToken(user, client, config.secrets.refreshToken);
                                var rspTokens = {};
                                rspTokens.access_token = generateToken(user, client, config.secrets.accessToken, config.token.expiresInMinutes);
                                var encryptedRefToken = cryptography.encrypt(refreshToken);

                                var token = {
                                    clientId: client._id,
                                    refreshToken: refreshToken
                                };

                                UserModel.update({
                                    _id: user._id
                                }, {
                                        $push: {
                                            'tokens': token
                                        }
                                    }, function(err, numAffected) {
                                        if (err) {
                                            console.log(err);
                                            sendRsp(res, 400, err);
                                        }
                                        res.cookie("staffing_refresh_token", encryptedRefToken);
                                        sendRsp(res, 200, 'Success', rspTokens);
                                    });
                            } else {
                                if (err.code == 11000) {
                                    return sendRsp(res, 409, "User already exists");
                                } else {
                                    return sendRsp(res, 500, "User create error");
                                }
                            }
                        });
                    }
                });
            }
        });
    });
};