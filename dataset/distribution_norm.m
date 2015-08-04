function Point = distribution_norm(p,sigma,nop)

if nargin <3
    nop=500;
end

sz = size(p(:));
centernum = length(p);
dim       = sz(1)/length(p);
Point = zeros(centernum*nop,dim);
for i=1:centernum
    for j=1:nop
       disp = randn([1,dim]);
       %y_disp = randn([1,dim]);
       idx = j+(i-1)*nop;
       Point(idx,:) = sigma* disp(1,:) + p(i,:);
       %Point(idx,2) = sigma* y_disp + p(i,2);
    end
   plot(Point(:,1),Point(:,2),'r.');
   
end
    

end
