export const config = {
  matcher: '/',
};

export default function middleware(request) {
  const url = new URL(request.url);
  const hostname = request.headers.get('host');

  // deck.trinitycorelabs.com 접속 시
  if (hostname && hostname.includes('deck.trinitycorelabs.com')) {
    url.pathname = '/deck.html';
  } 
  // 그 외 모든 도메인 접속 시
  else {
    url.pathname = '/landing.html';
  }

  return Response.rewrite(url);
}
