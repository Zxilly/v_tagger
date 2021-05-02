var apiurl

if (process.env.NODE_ENV === 'production') {
    apiurl = "https://vt.api.learningman.top"
} else {
    apiurl = "http://localhost:14562"
}

export {apiurl}
