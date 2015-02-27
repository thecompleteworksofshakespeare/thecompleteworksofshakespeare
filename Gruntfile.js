module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    aws: grunt.file.readJSON('private/aws.json'),
    aws_s3: {
      options: {
        accessKeyId: '<%= aws.AWSAccessKeyId %>', // Use the variables
        secretAccessKey: '<%= aws.AWSSecretKey %>', // You can also use env variables
        region: 'us-east-1',
        uploadConcurrency: 5, // 5 simultaneous uploads
        downloadConcurrency: 5 // 5 simultaneous downloads
      },
      prod: {
        options: {
          bucket: 'www.thecompleteworksofshakespeare.com',
          //differential: true // Only uploads the files that have changed
        },
        files: [
            {expand: true, cwd: 'output', src: ['**'], dest: ''},
        ]
      }
    },
  });

  // Load plugins
  grunt.loadNpmTasks('grunt-aws-s3');

};
